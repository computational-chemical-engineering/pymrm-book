"""Add per-page PDF downloads to a built MyST/Jupyter Book site.

Run this after ``jupyter-book build --html`` and before uploading the
``_build/html`` directory. The script renders every generated HTML page to a
matching PDF under ``downloads/pdf/`` and injects a small JavaScript helper that
adds a PDF download link beside the existing MyST download button.
"""

from __future__ import annotations

import argparse
import contextlib
import functools
import http.server
import os
import posixpath
import socketserver
import threading
from pathlib import Path
from urllib.parse import unquote, urlsplit


PDF_HELPER_JS = r"""
(function () {
  function normalizeBase(value) {
    if (!value || value === "/") return "";
    return value.replace(/\/+$/, "");
  }

  const config = window.__MYST_PAGE_PDF_DOWNLOADS__ || {};
  const baseUrl = normalizeBase(config.baseUrl || "");

  function routePath() {
    let path = window.location.pathname.replace(/\/+$/, "");
    if (baseUrl && path === baseUrl) path = "/";
    if (baseUrl && path.startsWith(baseUrl + "/")) path = path.slice(baseUrl.length);
    if (!path) path = "/";
    return path;
  }

  function pdfHref() {
    const route = routePath();
    const pdfPath = route === "/" ? "/downloads/pdf/index.pdf" : "/downloads/pdf" + route + ".pdf";
    return baseUrl + pdfPath;
  }

  function ensureDirectLink() {
    const dropdown = document.querySelector(".myst-fm-downloads-dropdown");
    if (!dropdown || document.querySelector(".myst-fm-pdf-download-link")) return;

    const link = document.createElement("a");
    link.className = "myst-fm-pdf-download-link relative ml-2 -mr-1";
    link.href = pdfHref();
    link.download = "";
    link.title = "Download this page as PDF";
    link.setAttribute("aria-label", "Download this page as PDF");
    link.innerHTML = '<span class="sr-only">Download PDF</span><span aria-hidden="true" style="font-size:0.75rem;font-weight:600;line-height:1.25rem">PDF</span>';
    dropdown.insertAdjacentElement("afterend", link);
  }

  function ensureMenuItem() {
    const menu = document.querySelector('[role="menu"], [data-headlessui-state~="open"]');
    if (!menu || menu.querySelector(".myst-fm-pdf-download-menu-item")) return;
    const item = document.createElement("a");
    item.className = "myst-fm-pdf-download-menu-item block px-4 py-2 text-sm no-underline";
    item.href = pdfHref();
    item.download = "";
    item.setAttribute("role", "menuitem");
    item.textContent = "PDF";
    menu.appendChild(item);
  }

  function install() {
    ensureDirectLink();
    ensureMenuItem();
  }

  const style = document.createElement("style");
  style.textContent = ".myst-fm-pdf-download-link{display:inline-flex;align-items:center;color:inherit;text-decoration:none}.myst-fm-pdf-download-link:hover{text-decoration:underline}";
  document.head.appendChild(style);

  install();
  new MutationObserver(install).observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener("popstate", install);
})();
"""


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


def inject_helper(html_dir: Path, base_url: str) -> int:
    build_dir = html_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    helper_path = build_dir / "page-pdf-downloads.js"
    helper_path.write_text(PDF_HELPER_JS.strip() + "\n", encoding="utf-8")

    base = normalize_base_url(base_url)
    snippet = (
        f'<script>window.__MYST_PAGE_PDF_DOWNLOADS__={{baseUrl:{base!r}}};</script>'
        f'<script src="{base}/build/page-pdf-downloads.js" defer></script>'
    )
    count = 0
    for html_file in iter_pages(html_dir):
        html = html_file.read_text(encoding="utf-8")
        if "page-pdf-downloads.js" in html:
            continue
        if "</body>" in html:
            html = html.replace("</body>", snippet + "</body>", 1)
        else:
            html += snippet
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
    injected = inject_helper(html_dir, args.base_url)
    print(f"Rendered {rendered} page PDF(s); injected helper into {injected} HTML page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
