"""Regenerate content/api/alphabetical_overview.md and content/api/api.md.

Uses ``pymrm.__all__`` as the single source of truth so that renamed or
removed symbols are automatically dropped and newly added public symbols are
automatically included.  Run this script after bumping the pymrm submodule::

    pip install ./pymrm
    python3 scripts/generate_function_list.py
"""

import importlib
import inspect
import re
from pathlib import Path

import pymrm


def strip_sphinx_roles(text):
    """Remove Sphinx cross-reference roles like :mod:`pymrm` → `pymrm`."""
    return re.sub(r":(mod|class|func|meth|attr|exc|obj|ref|doc):`([^`]*)`", r"`\2`", text)


def slugify_symbol(qualified_name):
    """Create a stable filename stem for a fully-qualified symbol name."""
    return re.sub(r"[^0-9A-Za-z._-]+", "-", qualified_name)


def get_clean_docstring(obj):
    """Return a role-stripped docstring for markdown rendering."""
    doc = inspect.getdoc(obj) or ""
    return strip_sphinx_roles(doc)


def get_source_code(obj):
    """Best-effort source extraction for implementation display."""
    try:
        return inspect.getsource(obj)
    except (OSError, TypeError):
        return ""


REPO_ROOT = Path(__file__).resolve().parent.parent
API_DIR = REPO_ROOT / "content" / "api"
MODULES_DIR = API_DIR / "modules"
SYMBOLS_DIR = API_DIR / "symbols"

for generated_dir in (MODULES_DIR, SYMBOLS_DIR):
    generated_dir.mkdir(parents=True, exist_ok=True)
    for old_file in generated_dir.glob("*.md"):
        old_file.unlink()

# ---------------------------------------------------------------------------
# Build the qualified symbol list from pymrm.__all__.
# obj.__module__ gives the submodule where the symbol is actually defined.
# ---------------------------------------------------------------------------
all_items = []
for name in pymrm.__all__:
    obj = getattr(pymrm, name, None)
    if obj is None:
        continue
    mod_name = getattr(obj, "__module__", None)
    if mod_name and mod_name.startswith("pymrm."):
        doc = inspect.getdoc(obj) or ""
        first_line = doc.split("\n")[0] if doc else ""
        first_line = strip_sphinx_roles(first_line)
        sig = ""
        try:
            sig = str(inspect.signature(obj))
        except (ValueError, TypeError):
            pass
        all_items.append(
            {
                "qualified": f"{mod_name}.{name}",
                "name": name,
                "module": mod_name,
                "doc": first_line,
                "sig": sig,
                "is_class": inspect.isclass(obj),
                "object": obj,
            }
        )

all_items = sorted(all_items, key=lambda item: item["qualified"])

# ---------------------------------------------------------------------------
# Derive the ordered list of unique submodules for the modules overview page.
# ---------------------------------------------------------------------------
module_names = sorted({item["module"] for item in all_items})

# ---------------------------------------------------------------------------
# Generate detail pages for every module and symbol.
# ---------------------------------------------------------------------------
for mod_name in module_names:
    module_page = MODULES_DIR / f"{slugify_symbol(mod_name)}.md"
    mod = importlib.import_module(mod_name)
    mod_doc = get_clean_docstring(mod)
    with module_page.open("w") as f:
        f.write(f"# `{mod_name}`\n\n")
        if mod_doc:
            f.write("## Docstring\n\n")
            f.write("```text\n")
            f.write(f"{mod_doc}\n")
            f.write("```\n\n")

for item in all_items:
    symbol_page = SYMBOLS_DIR / f"{slugify_symbol(item['qualified'])}.md"
    full_doc = get_clean_docstring(item["object"])
    source_code = get_source_code(item["object"])
    with symbol_page.open("w") as f:
        f.write(f"# `{item['qualified']}`\n\n")
        if item["sig"]:
            f.write("## Signature\n\n")
            f.write(f"`{item['qualified']}{item['sig']}`\n\n")
        if full_doc:
            f.write("## Docstring\n\n")
            f.write("```text\n")
            f.write(f"{full_doc}\n")
            f.write("```\n\n")
        if source_code:
            f.write("## Implementation\n\n")
            f.write("```python\n")
            f.write(f"{source_code}\n")
            f.write("```\n")
        else:
            f.write("## Implementation\n\n")
            f.write("_Source code is not available via Python introspection._\n")

# ---------------------------------------------------------------------------
# Write content/api/alphabetical_overview.md
# ---------------------------------------------------------------------------
with (API_DIR / "alphabetical_overview.md").open("w") as f:
    f.write("# All Functions and Classes\n\n")
    f.write(
        "An overview of all functions and classes in the `pymrm` package.\n\n"
    )
    f.write("| Name | Description |\n")
    f.write("| ---- | ----------- |\n")
    for item in all_items:
        symbol_link = f"symbols/{slugify_symbol(item['qualified'])}.md"
        f.write(f"| [`{item['qualified']}`]({symbol_link}) | {item['doc']} |\n")

# ---------------------------------------------------------------------------
# Write content/api/api.md
# ---------------------------------------------------------------------------
with (API_DIR / "api.md").open("w") as f:
    f.write("# Modules\n\n")
    f.write("An overview of all modules of the `pymrm` package.\n\n")
    for mod_name in module_names:
        mod = importlib.import_module(mod_name)
        mod_doc = get_clean_docstring(mod)
        first_line = mod_doc.split("\n")[0] if mod_doc else ""
        module_link = f"modules/{slugify_symbol(mod_name)}.md"
        f.write(f"## [`{mod_name}`]({module_link})\n\n")
        if first_line:
            f.write(f"{first_line}\n\n")
        # List functions in this module
        mod_items = [i for i in all_items if i["module"] == mod_name]
        if mod_items:
            f.write("| Function / Class | Description |\n")
            f.write("| ---------------- | ----------- |\n")
            for item in mod_items:
                symbol_link = f"symbols/{slugify_symbol(item['qualified'])}.md"
                f.write(f"| [`{item['name']}`]({symbol_link}) | {item['doc']} |\n")
            f.write("\n")
