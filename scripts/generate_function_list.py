"""Regenerate content/api/alphabetical_overview.rst and content/api/api.rst.

Uses ``pymrm.__all__`` as the single source of truth so that renamed or
removed symbols are automatically dropped and newly added public symbols are
automatically included.  Run this script after bumping the pymrm submodule::

    pip install ./pymrm
    python3 scripts/generate_function_list.py
"""

import importlib

import pymrm

# ---------------------------------------------------------------------------
# Build the qualified symbol list from pymrm.__all__.
# obj.__module__ gives the submodule where the symbol is actually defined,
# which is the correct toctree target for autosummary.
# ---------------------------------------------------------------------------
all_items = []
for name in pymrm.__all__:
    obj = getattr(pymrm, name, None)
    if obj is None:
        continue
    mod_name = getattr(obj, "__module__", None)
    if mod_name and mod_name.startswith("pymrm."):
        all_items.append(f"{mod_name}.{name}")

all_items = sorted(all_items)

# ---------------------------------------------------------------------------
# Derive the ordered list of unique submodules for the modules overview page.
# ---------------------------------------------------------------------------
module_names = sorted({item.rsplit(".", 1)[0] for item in all_items})

# ---------------------------------------------------------------------------
# Write content/api/alphabetical_overview.rst
# ---------------------------------------------------------------------------
with open("content/api/alphabetical_overview.rst", "w") as f:
    f.write("Alphabetical Overview\n")
    f.write("=====================\n\n")
    f.write("An overview of all functions and classes in the ``pymrm`` package.\n\n")
    f.write(".. autosummary::\n")
    f.write("   :toctree: generated/all\n")
    f.write("   :nosignatures:\n\n")
    for item in all_items:
        f.write(f"   {item}\n")

# ---------------------------------------------------------------------------
# Write content/api/api.rst
# ---------------------------------------------------------------------------
with open("content/api/api.rst", "w") as f:
    f.write("Modules\n")
    f.write("=======\n\n")
    f.write("An overview of all modules of the ``pymrm`` package.\n\n")
    f.write(".. autosummary::\n")
    f.write("   :toctree: overview\n")
    f.write("   :nosignatures:\n\n")
    for mod_name in module_names:
        f.write(f"   {mod_name}\n")
