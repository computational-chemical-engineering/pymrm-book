"""Regenerate the PyMRM API reference from source docstrings.

After updating the `pymrm` submodule, install both the package and docs
dependencies before regenerating the API pages::

    pip install ./pymrm
    pip install -r requirements.txt
    python3 scripts/generate_function_list.py
"""

from __future__ import annotations

import re
import subprocess
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from autodoc2.analysis import analyse_module
from autodoc2.utils import yield_modules
import pymrm


REPO_ROOT = Path(__file__).resolve().parent.parent
PYMRM_ROOT = REPO_ROOT / "pymrm"
PYMRM_SRC = PYMRM_ROOT / "src" / "pymrm"
API_DIR = REPO_ROOT / "content" / "api"
MODULES_DIR = API_DIR / "modules"
SYMBOLS_DIR = API_DIR / "symbols"
GITHUB_REPO = "https://github.com/computational-chemical-engineering/pymrm"

STRUCTURED_SECTIONS = {
    "Parameters",
    "Returns",
    "Yields",
    "Raises",
    "Attributes",
    "Methods",
}
PUBLIC_TYPES = {"function", "class"}
CLASS_CHILD_TYPES = {"method", "property", "attribute"}
SIGNATURE_TYPES = {"function", "class", "method"}
SPHINX_ROLE_RE = re.compile(r":(mod|class|func|meth|attr|exc|obj|ref|doc):`([^`]*)`")


def slugify_symbol(qualified_name: str) -> str:
    """Create a stable filename stem for a fully-qualified symbol name."""
    return re.sub(r"[^0-9A-Za-z._-]+", "-", qualified_name)


def split_summary(doc: str) -> tuple[str, str]:
    """Return the first paragraph and the remaining docstring content."""
    clean = normalize_docstring(doc)
    if not clean:
        return "", ""
    paragraphs = re.split(r"\n\s*\n", clean, maxsplit=1)
    summary = paragraphs[0].replace("\n", " ").strip()
    remainder = paragraphs[1].strip() if len(paragraphs) > 1 else ""
    return summary, remainder


def normalize_docstring(doc: str) -> str:
    """Normalize a docstring for markdown rendering."""
    clean = textwrap.dedent(doc or "").strip("\n")
    if not clean:
        return ""
    clean = SPHINX_ROLE_RE.sub(r"`\2`", clean)
    lines = clean.splitlines()
    if (
        len(lines) > 1
        and lines[0].strip()
        and set(lines[1].strip()) == {"="}
        and len(lines[1].strip()) >= len(lines[0].strip())
    ):
        lines = lines[2:]
    return "\n".join(lines).strip()


def iter_section_blocks(lines: list[str]) -> Iterable[tuple[str | None, list[str]]]:
    """Split a docstring into free-form text and NumPy-style sections."""
    block: list[str] = []
    section_name: str | None = None
    i = 0
    while i < len(lines):
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        if (
            line.strip()
            and set(next_line.strip()) == {"-"}
            and len(next_line.strip()) >= len(line.strip())
        ):
            if block:
                yield section_name, block
                block = []
            section_name = line.strip()
            i += 2
            continue
        block.append(line)
        i += 1
    if block:
        yield section_name, block


def render_text_block(lines: list[str]) -> list[str]:
    """Render a free-form docstring block as markdown paragraphs."""
    content = "\n".join(lines).strip("\n")
    return content.splitlines() if content else []


def render_structured_section(lines: list[str]) -> list[str]:
    """Render a NumPy-style parameter/returns section as a markdown list."""
    entries: list[tuple[str, list[str]]] = []
    header: str | None = None
    description: list[str] = []
    for line in lines:
        if not line.strip():
            if header is not None:
                description.append("")
            continue
        if line == line.lstrip():
            if header is not None:
                entries.append((header, description))
            header = line.strip()
            description = []
        else:
            description.append(line)
    if header is not None:
        entries.append((header, description))

    rendered: list[str] = []
    for header, description in entries:
        if " : " in header:
            name, type_name = header.split(" : ", 1)
            rendered.append(f"- `{name.strip()}` (*{type_name.strip()}*)")
        else:
            rendered.append(f"- `{header.strip()}`")
        clean_description = textwrap.dedent("\n".join(description)).strip()
        if clean_description:
            for desc_line in clean_description.splitlines():
                if desc_line:
                    rendered.append(f"  {desc_line}")
                else:
                    rendered.append("")
        rendered.append("")
    while rendered and not rendered[-1].strip():
        rendered.pop()
    return rendered


def render_docstring(doc: str, heading_level: int = 2) -> list[str]:
    """Convert a docstring into markdown."""
    clean = normalize_docstring(doc)
    if not clean:
        return []

    rendered: list[str] = []
    for section_name, block in iter_section_blocks(clean.splitlines()):
        if section_name is None:
            rendered.extend(render_text_block(block))
        else:
            rendered.extend([f"{'#' * heading_level} {section_name}", ""])
            if section_name in STRUCTURED_SECTIONS:
                rendered.extend(render_structured_section(block))
            else:
                rendered.extend(render_text_block(block))
        if rendered and rendered[-1] != "":
            rendered.append("")

    while rendered and not rendered[-1].strip():
        rendered.pop()
    return rendered


def format_signature(item: dict, items: dict[str, dict] | None = None) -> str:
    """Format an analysed function/class signature."""
    if item["type"] not in SIGNATURE_TYPES:
        return ""

    signature_item = item
    if item["type"] == "class" and items is not None:
        signature_item = items.get(f"{item['full_name']}.__init__", item)

    parts = []
    for prefix, name, annotation, default in signature_item.get("args", []):
        token = ""
        if prefix:
            token += prefix
        if name:
            token += name
        if annotation:
            token += f": {annotation}"
        if default is not None:
            token += f" = {default}"
        parts.append(token)

    short_name = item["full_name"].split(".")[-1]
    signature = f"{short_name}({', '.join(parts)})"
    if item["type"] != "class" and signature_item.get("return_annotation"):
        signature += f" -> {signature_item['return_annotation']}"
    return signature


def get_source_excerpt(item: dict) -> str:
    """Extract the source text for an analysed item."""
    if "range" not in item or "file_path" not in item:
        return ""
    start, end = item["range"]
    lines = Path(item["file_path"]).read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1 : end]).rstrip()


def get_source_url(item: dict, commit_sha: str) -> str:
    """Build a GitHub source link for an analysed item."""
    file_path = Path(item["file_path"]).resolve()
    rel_path = file_path.relative_to(PYMRM_ROOT).as_posix()
    url = f"{GITHUB_REPO}/blob/{commit_sha}/{rel_path}"
    if "range" in item:
        start, end = item["range"]
        url += f"#L{start}-L{end}"
    return url


def get_direct_children(items: dict[str, dict], parent_name: str, types: set[str]) -> list[dict]:
    """Return immediate child members of a class."""
    prefix = f"{parent_name}."
    children = []
    for full_name, item in items.items():
        if item["type"] not in types or not full_name.startswith(prefix):
            continue
        remainder = full_name[len(prefix) :]
        if "." not in remainder:
            children.append(item)
    order = {"method": 0, "property": 1, "attribute": 2}

    def sort_key(item: dict) -> tuple[int, int, str]:
        name = item["full_name"].split(".")[-1]
        special_order = 0 if name == "__init__" else 1 if name == "__call__" else 2
        return order[item["type"]], special_order, name

    return sorted(children, key=sort_key)


def analyse_package() -> dict[str, dict]:
    """Analyse the package source tree with Autodoc2."""
    items: dict[str, dict] = {}
    for module_path, module_name in yield_modules(PYMRM_SRC, root_module="pymrm"):
        for item in analyse_module(module_path, module_name):
            item.setdefault("file_path", str(module_path))
            items[item["full_name"]] = item
    return items


def get_commit_sha() -> str:
    """Return the checked-out pymrm submodule commit SHA."""
    try:
        return (
            subprocess.check_output(
                ["git", "-C", str(PYMRM_ROOT), "rev-parse", "HEAD"], text=True
            )
            .strip()
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Unable to determine the pinned pymrm revision. "
            "Ensure the pymrm submodule is initialized before generating API docs."
        ) from exc


def write_text(path: Path, lines: list[str]) -> None:
    """Write a markdown file with a trailing newline."""
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def render_class_children(item: dict, items: dict[str, dict], commit_sha: str) -> list[str]:
    """Render methods and attributes for a public class."""
    children = get_direct_children(items, item["full_name"], CLASS_CHILD_TYPES)
    if not children:
        return []

    lines = ["## Members", ""]
    for child in children:
        signature = (
            format_signature(child, items)
            if child["type"] == "method"
            else child["full_name"].split(".")[-1]
        )
        if child["type"] == "method":
            lines.append(f"### `{signature}`")
        else:
            lines.append(f"### `{child['full_name'].split('.')[-1]}`")
        lines.append("")

        child_summary, child_remainder = split_summary(child.get("doc", ""))
        if child_summary:
            lines.extend([child_summary, ""])
        if child_remainder:
            lines.extend(render_docstring(child_remainder, heading_level=4))
            lines.append("")

        if "file_path" in child:
            lines.extend(
                [
                    f"[View source on GitHub]({get_source_url(child, commit_sha)})",
                    "",
                ]
            )
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def render_module_page(
    module_name: str,
    module_item: dict,
    module_public_items: list[dict],
    items: dict[str, dict],
    commit_sha: str,
) -> list[str]:
    """Render a single module reference page."""
    lines = [
        f"# `{module_name}`",
        "",
        "[Back to modules overview](../api)",
        "",
    ]

    summary, remainder = split_summary(module_item.get("doc", ""))
    if summary:
        lines.extend([summary, ""])
    if remainder:
        lines.extend(render_docstring(remainder, heading_level=2))
        lines.append("")

    lines.extend(
        [
            f"[View module source on GitHub]({get_source_url(module_item, commit_sha)})",
            "",
            "## Public API",
            "",
            "| Symbol | Type | Summary |",
            "| ------ | ---- | ------- |",
        ]
    )
    for item in module_public_items:
        symbol_link = f"../symbols/{slugify_symbol(item['full_name'])}"
        summary, _ = split_summary(item.get("doc", ""))
        lines.append(
            f"| [`{item['full_name'].split('.')[-1]}`]({symbol_link}) | "
            f"{item['type']} | {summary or '—'} |"
        )
    lines.append("")

    for item in module_public_items:
        signature = format_signature(item, items)
        lines.extend(
            [
                f"## `{signature or item['full_name'].split('.')[-1]}`",
                "",
                f"[Open dedicated reference page](../symbols/{slugify_symbol(item['full_name'])})",
                "",
            ]
        )
        summary, remainder = split_summary(item.get("doc", ""))
        if summary:
            lines.extend([summary, ""])
        if remainder:
            lines.extend(render_docstring(remainder, heading_level=3))
            lines.append("")
        lines.extend(
            [
                f"[View source on GitHub]({get_source_url(item, commit_sha)})",
                "",
            ]
        )
        if item["type"] == "class":
            class_children = render_class_children(item, items, commit_sha)
            if class_children:
                lines.extend(class_children)
                lines.append("")

    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def render_symbol_page(item: dict, items: dict[str, dict], commit_sha: str) -> list[str]:
    """Render a single function/class page."""
    module_name = item["full_name"].rsplit(".", 1)[0]
    signature = format_signature(item, items)
    lines = [
        f"# `{item['full_name']}`",
        "",
        f"[Back to module page](../modules/{slugify_symbol(module_name)}) · "
        "[Back to alphabetical overview](../alphabetical_overview)",
        "",
    ]

    if signature:
        lines.extend(["## Signature", "", f"`{signature}`", ""])

    summary, remainder = split_summary(item.get("doc", ""))
    if summary:
        lines.extend(["## Summary", "", summary, ""])
    if remainder:
        lines.extend(["## Documentation", ""])
        lines.extend(render_docstring(remainder, heading_level=3))
        lines.append("")

    lines.extend(
        [
            "## Source",
            "",
            f"[View on GitHub]({get_source_url(item, commit_sha)})",
            "",
        ]
    )
    source_code = get_source_excerpt(item)
    if source_code:
        lines.extend(["```python", source_code, "```", ""])

    if item["type"] == "class":
        class_children = render_class_children(item, items, commit_sha)
        if class_children:
            lines.extend(class_children)
            lines.append("")

    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def main() -> None:
    """Generate the API reference markdown pages."""
    items = analyse_package()
    commit_sha = get_commit_sha()

    for generated_dir in (MODULES_DIR, SYMBOLS_DIR):
        generated_dir.mkdir(parents=True, exist_ok=True)
        for old_file in generated_dir.glob("*.md"):
            old_file.unlink()

    public_items = []
    for name in pymrm.__all__:
        obj = getattr(pymrm, name, None)
        module_name = getattr(obj, "__module__", None)
        if not module_name or module_name.startswith("pymrm._"):
            continue
        full_name = f"{module_name}.{name}"
        item = items.get(full_name)
        if item and item["type"] in PUBLIC_TYPES:
            public_items.append(item)

    public_items.sort(key=lambda item: item["full_name"])
    module_names = sorted({item["full_name"].rsplit(".", 1)[0] for item in public_items})
    public_items_by_module: dict[str, list[dict]] = defaultdict(list)
    for item in public_items:
        public_items_by_module[item["full_name"].rsplit(".", 1)[0]].append(item)

    for module_name in module_names:
        module_item = items[module_name]
        module_path = MODULES_DIR / f"{slugify_symbol(module_name)}.md"
        write_text(
            module_path,
            render_module_page(
                module_name,
                module_item,
                public_items_by_module[module_name],
                items,
                commit_sha,
            ),
        )

    for item in public_items:
        symbol_path = SYMBOLS_DIR / f"{slugify_symbol(item['full_name'])}.md"
        write_text(symbol_path, render_symbol_page(item, items, commit_sha))

    api_lines = [
        "# Modules",
        "",
        "Autogenerated module reference for the public `pymrm` API.",
        "",
        "Each module page expands the package docstrings into navigable documentation and links back to the implementation in the pinned `pymrm` submodule.",
    ]
    api_lines.append("")

    for module_name in module_names:
        module_item = items[module_name]
        summary, _ = split_summary(module_item.get("doc", ""))
        api_lines.extend(
            [
                f"## [`{module_name}`](modules/{slugify_symbol(module_name)})",
                "",
                summary or "Autogenerated module reference.",
                "",
                "| Symbol | Type | Summary |",
                "| ------ | ---- | ------- |",
            ]
        )
        for item in public_items_by_module[module_name]:
            symbol_link = f"symbols/{slugify_symbol(item['full_name'])}"
            item_summary, _ = split_summary(item.get("doc", ""))
            api_lines.append(
                f"| [`{item['full_name'].split('.')[-1]}`]({symbol_link}) | "
                f"{item['type']} | {item_summary or '—'} |"
            )
        api_lines.append("")
    write_text(API_DIR / "api.md", api_lines)

    alpha_lines = [
        "# All Functions and Classes",
        "",
        "Alphabetical index of the public PyMRM API with direct links to source-backed reference pages.",
    ]
    alpha_lines.extend(["", "| Name | Module | Summary |", "| ---- | ------ | ------- |"])
    for item in public_items:
        summary, _ = split_summary(item.get("doc", ""))
        alpha_lines.append(
            f"| [`{item['full_name']}`](symbols/{slugify_symbol(item['full_name'])}) | "
            f"`{item['full_name'].rsplit('.', 1)[0]}` | {summary or '—'} |"
        )
    write_text(API_DIR / "alphabetical_overview.md", alpha_lines)


if __name__ == "__main__":
    main()
