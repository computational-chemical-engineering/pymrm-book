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

import pymrm


def strip_sphinx_roles(text):
    """Remove Sphinx cross-reference roles like :mod:`pymrm` → `pymrm`."""
    return re.sub(r":(mod|class|func|meth|attr|exc|obj|ref|doc):`([^`]*)`", r"`\2`", text)

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
        all_items.append((f"{mod_name}.{name}", name, first_line, sig))

all_items = sorted(all_items)

# ---------------------------------------------------------------------------
# Derive the ordered list of unique submodules for the modules overview page.
# ---------------------------------------------------------------------------
module_names = sorted({item[0].rsplit(".", 1)[0] for item in all_items})

# ---------------------------------------------------------------------------
# Write content/api/alphabetical_overview.md
# ---------------------------------------------------------------------------
with open("content/api/alphabetical_overview.md", "w") as f:
    f.write("# All Functions and Classes\n\n")
    f.write(
        "An overview of all functions and classes in the `pymrm` package.\n\n"
    )
    f.write("| Name | Description |\n")
    f.write("| ---- | ----------- |\n")
    for qualified, name, doc, sig in all_items:
        f.write(f"| `{qualified}` | {doc} |\n")

# ---------------------------------------------------------------------------
# Write content/api/api.md
# ---------------------------------------------------------------------------
with open("content/api/api.md", "w") as f:
    f.write("# Modules\n\n")
    f.write("An overview of all modules of the `pymrm` package.\n\n")
    for mod_name in module_names:
        mod = importlib.import_module(mod_name)
        mod_doc = inspect.getdoc(mod) or ""
        first_line = mod_doc.split("\n")[0] if mod_doc else ""
        first_line = strip_sphinx_roles(first_line)
        f.write(f"## `{mod_name}`\n\n")
        if first_line:
            f.write(f"{first_line}\n\n")
        # List functions in this module
        mod_items = [i for i in all_items if i[0].startswith(mod_name + ".")]
        if mod_items:
            f.write("| Function / Class | Description |\n")
            f.write("| ---------------- | ----------- |\n")
            for qualified, name, doc, sig in mod_items:
                f.write(f"| `{name}` | {doc} |\n")
            f.write("\n")
