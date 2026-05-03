"""Add per-page PDF downloads to a built MyST/Jupyter Book site.

Run this after ``jupyter-book build --html`` and before uploading the
``_build/html`` directory. The script renders every generated HTML page to a
matching PDF under ``downloads/pdf/`` and adds the PDF to each page's MyST export
metadata, so the existing download menu offers both Markdown and PDF versions.
"""

from __future__ import annotations

import argparse
import contextlib
import functools
import http.server
import json
import os
import posixpath
import re
import socketserver
import threading
from pathlib import Path
from urllib.parse import unquote, urlsplit


REMIX_CONTEXT_RE = re.compile(r"window\.__remixContext\s*=\s*(\{.*?\});</script>", re.DOTALL)


class BasePathHandler(http.server.SimpleHTTPRequestHandler):
    """Serve a directory while accepting an optional GitHub Pages base path."""

    def __init__(self, *args, directory: str, base_url: str, **kwargs):
        self.base_url = normalize_base_url(base_url)
        super().__init__(*args, directory=directory, **kwargs)

    def translate_path(self, path: str) -> str:
        split = urlsplit(path)
        request_path = posixpath.normpath(unquote(split.path))
        if self.base_url and request_path == self.base_url:
            request_path = "/"
        elif self.base_url and request_path.startswith(self.base_url + "/"):
            request_path = request_path[len(self.base_url) :]
        return super().translate_path(request_path)

    def log_message(self, format: str, *args: object) -> None:
        return


def normalize_base_url(base_url: str) -> str:
    base_url = (base_url or "").strip()
    if not base_url or base_url == "/":
        return ""
    return "/" + base_url.strip("/")


def page_route(html_dir: Path, html_file: Path) -> str:
    rel = html_file.relative_to(html_dir).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("/index.html")]
    if rel.endswith(".html"):
        return "/" + rel[: -len(".html")]
    raise ValueError(f"Not an HTML page: {html_file}")


def pdf_path(html_dir: Path, route: str) -> Path:
    if route == "/":
        return html_dir / "downloads" / "pdf" / "index.pdf"
    return html_dir / "downloads" / "pdf" / (route.strip("/").replace("/", os.sep) + ".pdf")


def pdf_url(route: str, base_url: str) -> str:
    base = normalize_base_url(base_url)
    if route == "/":
        return f"{base}/downloads/pdf/index.pdf"
    return f"{base}/downloads/pdf{route}.pdf"


def pdf_filename(route: str) -> str:
    if route == "/":
        return "index.pdf"
    return f"{route.rstrip('/').rsplit('/', 1)[-1]}.pdf"


def iter_pages(html_dir: Path) -> list[Path]:
    pages: list[Path] = []
    for path in sorted(html_dir.rglob("*.html")):
        rel = path.relative_to(html_dir).parts
        if not rel:
            continue
        if rel[0] in {"build", "downloads"}:
            continue
        pages.append(path)
    return pages


@contextlib.contextmanager
def local_server(html_dir: Path, base_url: str):
    handler = functools.partial(
        BasePathHandler,
        directory=str(html_dir),
        base_url=base_url,
    )
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as httpd:
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{httpd.server_address[1]}"
        finally:
            httpd.shutdown()
            thread.join()


def render_pdfs(html_dir: Path, base_url: str, max_pages: int | None) -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "The 'playwright' package is required to create page PDFs. "
            "Install it and run 'python -m playwright install chromium'."
        ) from exc

    pages = iter_pages(html_dir)
    if max_pages is not None:
        pages = pages[:max_pages]

    with local_server(html_dir, base_url) as origin:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            for html_file in pages:
                route = page_route(html_dir, html_file)
                output = pdf_path(html_dir, route)
                output.parent.mkdir(parents=True, exist_ok=True)
                page.goto(f"{origin}{normalize_base_url(base_url)}{route}", wait_until="networkidle")
                page.pdf(
                    path=str(output),
                    format="A4",
                    print_background=True,
                    margin={"top": "18mm", "right": "15mm", "bottom": "18mm", "left": "15mm"},
                )
            browser.close()
    return len(pages)


def pdf_export(route: str, base_url: str) -> dict[str, str]:
    return {
        "format": "pdf",
        "filename": pdf_filename(route),
        "url": pdf_url(route, base_url),
    }


def add_pdf_export(frontmatter: dict[str, object], export: dict[str, str]) -> bool:
    exports = frontmatter.setdefault("exports", [])
    if not isinstance(exports, list):
        return False
    if any(item.get("format") == "pdf" for item in exports if isinstance(item, dict)):
        return False
    exports.append(export)
    return True


def extract_page_slug(html: str) -> str | None:
    match = re.search(r'"slug":"([^"]+)"\s*,\s*"location"', html)
    return match.group(1) if match else None


def update_page_json(json_file: Path, export: dict[str, str]) -> bool:
    data = json.loads(json_file.read_text(encoding="utf-8"))
    frontmatter = data.get("frontmatter")
    if not isinstance(frontmatter, dict):
        return False
    changed = add_pdf_export(frontmatter, export)
    if changed:
        json_file.write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    return changed


def update_remix_context(html: str, page_slug: str, export: dict[str, str]) -> tuple[str, bool]:
    match = REMIX_CONTEXT_RE.search(html)
    if not match:
        return html, False

    context = json.loads(match.group(1))
    changed = False

    def visit(value: object) -> None:
        nonlocal changed
        if isinstance(value, dict):
            if value.get("slug") == page_slug and isinstance(value.get("frontmatter"), dict):
                changed = add_pdf_export(value["frontmatter"], export) or changed
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(context)
    if not changed:
        return html, False

    replacement = (
        "window.__remixContext = "
        + json.dumps(context, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        + ";</script>"
    )
    return html[: match.start()] + replacement + html[match.end() :], True


def add_pdf_exports(html_dir: Path, base_url: str) -> int:
    count = 0
    for html_file in iter_pages(html_dir):
        route = page_route(html_dir, html_file)
        export = pdf_export(route, base_url)
        html = html_file.read_text(encoding="utf-8")
        page_slug = extract_page_slug(html)
        changed = False

        if page_slug:
            json_file = html_dir / f"{page_slug}.json"
            if json_file.exists():
                changed = update_page_json(json_file, export) or changed
            html, html_changed = update_remix_context(html, page_slug, export)
            changed = html_changed or changed

        if changed:
            html_file.write_text(html, encoding="utf-8", newline="\n")
            count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html-dir", type=Path, default=Path("_build/html"))
    parser.add_argument("--base-url", default=os.environ.get("BASE_URL", ""))
    parser.add_argument("--skip-pdfs", action="store_true", help="Only inject the PDF download helper.")
    parser.add_argument("--max-pages", type=int, help="Render only the first N pages; useful for smoke tests.")
    args = parser.parse_args(argv)

    html_dir = args.html_dir.resolve()
    if not html_dir.exists():
        raise SystemExit(f"HTML build directory does not exist: {html_dir}")

    rendered = 0
    if not args.skip_pdfs:
        rendered = render_pdfs(html_dir, args.base_url, args.max_pages)
    updated = add_pdf_exports(html_dir, args.base_url)
    print(f"Rendered {rendered} page PDF(s); added PDF export metadata to {updated} page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
