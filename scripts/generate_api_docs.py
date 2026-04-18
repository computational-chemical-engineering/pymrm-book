"""Generate MyST Markdown API documentation from pymrm using griffe.

Replaces generate_function_list.py for the mystmd-based jupyter-book 2.x build.

Usage (run from repo root after initializing the pymrm submodule):
    python scripts/generate_api_docs.py

Outputs:
    content/api/generated/all/pymrm.<module>.<name>.md   (one per public symbol)
    content/api/generated/overview/pymrm.<module>.md     (one per module)
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import griffe

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
OUT_ALL = Path("content/api/generated/all")
OUT_OVERVIEW = Path("content/api/generated/overview")
SEARCH_PATHS = ["pymrm/src", "pymrm", "."]

# ---------------------------------------------------------------------------
# Docstring formatting (NumPy style)
# ---------------------------------------------------------------------------

def _format_sections(sections) -> str:
    parts = []
    for section in sections:
        kind = section.kind.value
        if kind == "text":
            text = section.value.strip()
            if text:
                parts.append(text)
        elif kind == "parameters":
            items = []
            for p in section.value:
                ann = f" : `{p.annotation}`" if p.annotation else ""
                desc = p.description.strip() if p.description else ""
                items.append(f"- **{p.name}**{ann}" + (f" — {desc}" if desc else ""))
            if items:
                parts.append("**Parameters**\n\n" + "\n".join(items))
        elif kind == "returns":
            items = []
            for r in section.value:
                ann = f"`{r.annotation}`" if r.annotation else ""
                desc = r.description.strip() if r.description else ""
                label = f"**{r.name}** : " if r.name else ""
                items.append(f"- {label}{ann}" + (f" — {desc}" if desc else ""))
            if items:
                parts.append("**Returns**\n\n" + "\n".join(items))
        elif kind == "raises":
            items = []
            for e in section.value:
                desc = e.description.strip() if e.description else ""
                items.append(f"- **{e.annotation}**" + (f" — {desc}" if desc else ""))
            if items:
                parts.append("**Raises**\n\n" + "\n".join(items))
        elif kind == "examples":
            parts.append("**Examples**\n\n```python\n" + section.value.strip() + "\n```")
        elif kind in ("notes", "note"):
            parts.append("**Notes**\n\n" + section.value.strip())
        elif kind in ("references", "reference"):
            parts.append("**References**\n\n" + section.value.strip())
        elif kind == "attributes":
            items = []
            for a in section.value:
                ann = f" : `{a.annotation}`" if a.annotation else ""
                desc = a.description.strip() if a.description else ""
                items.append(f"- **{a.name}**{ann}" + (f" — {desc}" if desc else ""))
            if items:
                parts.append("**Attributes**\n\n" + "\n".join(items))
    return "\n\n".join(parts)


def _docstring_md(obj) -> str:
    if obj.docstring is None:
        return ""
    try:
        sections = obj.docstring.parse("numpy")
        return _format_sections(sections)
    except Exception:
        return obj.docstring.value.strip()


def _signature(obj) -> str:
    params = []
    for p in obj.parameters:
        s = p.name
        if p.annotation:
            s += f": {p.annotation}"
        if p.default:
            s += f" = {p.default}"
        params.append(s)
    ret = f" -> {obj.returns}" if getattr(obj, "returns", None) else ""
    return f"{obj.name}({', '.join(params)}){ret}"


# ---------------------------------------------------------------------------
# Page generators
# ---------------------------------------------------------------------------

def write_function_page(qname: str, obj, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    blocks = [f"# `{qname}`"]

    is_class = isinstance(obj, griffe.Class)

    if is_class:
        init = obj.members.get("__init__")
        if init and isinstance(init, griffe.Function):
            sig = _signature(init)
            sig = obj.name + sig[sig.index("("):]
            blocks.append(f"```python\n{sig}\n```")
            doc = _docstring_md(init) or _docstring_md(obj)
        else:
            doc = _docstring_md(obj)
        if doc:
            blocks.append(doc)

        public_methods = [
            (name, m)
            for name, m in sorted(obj.members.items())
            if isinstance(m, griffe.Function) and not name.startswith("_")
        ]
        if public_methods:
            blocks.append("## Methods")
            for mname, method in public_methods:
                blocks.append(f"### `{mname}`\n\n```python\n{_signature(method)}\n```")
                mdoc = _docstring_md(method)
                if mdoc:
                    blocks.append(mdoc)
    else:
        blocks.append(f"```python\n{_signature(obj)}\n```")
        doc = _docstring_md(obj)
        if doc:
            blocks.append(doc)

    (out_dir / f"{qname}.md").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def write_module_page(mod_qname: str, mod_obj, items: list[str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    blocks = [f"# `{mod_qname}`"]

    doc = _docstring_md(mod_obj)
    if doc:
        blocks.append(doc)

    def _resolve_obj(short_name):
        o = mod_obj.members.get(short_name)
        if isinstance(o, griffe.Alias):
            try:
                return o.target
            except Exception:
                return None
        return o

    classes = [q for q in items if isinstance(_resolve_obj(q.rsplit(".", 1)[-1]), griffe.Class)]
    funcs = [q for q in items if not isinstance(_resolve_obj(q.rsplit(".", 1)[-1]), griffe.Class)]

    if classes:
        rows = "\n".join(f"- [{q.rsplit('.', 1)[-1]}](../all/{q})" for q in classes)
        blocks.append("## Classes\n\n" + rows)

    if funcs:
        rows = "\n".join(f"- [{q.rsplit('.', 1)[-1]}](../all/{q})" for q in funcs)
        blocks.append("## Functions\n\n" + rows)

    (out_dir / f"{mod_qname}.md").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # Load pymrm with griffe (pure static AST analysis — no import required)
    package = None
    for sp in SEARCH_PATHS:
        try:
            package = griffe.load("pymrm", search_paths=[sp])
            print(f"Loaded pymrm via griffe (search_path={sp!r})")
            break
        except Exception:
            continue

    if package is None:
        print("ERROR: griffe could not locate pymrm source. "
              "Ensure the pymrm submodule is initialized.", file=sys.stderr)
        sys.exit(1)

    # Use griffe's __all__ (pkg.exports) — no dynamic import needed
    exports = [name for name in (package.exports or []) if not name.startswith("_")]
    print(f"Found {len(exports)} public exports via griffe")

    # Build (qualified_name -> Function/Class) map
    all_items: list[str] = []
    obj_map: dict[str, griffe.Function | griffe.Class] = {}

    for name in exports:
        alias = package.members.get(name)
        if alias is None or not isinstance(alias, griffe.Alias):
            continue
        target_path = alias.target_path  # e.g. "pymrm.convect.construct_convflux_upwind"
        if not target_path.startswith("pymrm.") or target_path.count(".") < 2:
            continue
        parts = target_path.split(".")
        mod_short = parts[1]          # "convect"
        func_short = parts[-1]        # "construct_convflux_upwind"
        mod_obj = package.members.get(mod_short)
        if not isinstance(mod_obj, griffe.Module):
            continue
        func_obj = mod_obj.members.get(func_short)
        if func_obj is None:
            continue
        # Resolve alias if needed
        if isinstance(func_obj, griffe.Alias):
            try:
                func_obj = func_obj.target
            except Exception:
                print(f"  WARN: could not resolve {target_path}, skipping")
                continue
        if not isinstance(func_obj, (griffe.Function, griffe.Class)):
            continue
        all_items.append(target_path)
        obj_map[target_path] = func_obj

    all_items = sorted(all_items)
    print(f"Resolved {len(all_items)} symbols")

    # Group by module
    by_module: dict[str, list[str]] = defaultdict(list)
    for qname in all_items:
        mod = qname.rsplit(".", 1)[0]
        by_module[mod].append(qname)

    # Generate individual pages
    for qname in all_items:
        write_function_page(qname, obj_map[qname], OUT_ALL)
    print(f"Generated {len(all_items)} symbol pages in {OUT_ALL}/")

    # Generate module overview pages
    module_names = sorted(by_module.keys())
    for mod_qname in module_names:
        mod_short = mod_qname.split(".", 1)[1]
        mod_obj = package.members.get(mod_short)
        if not isinstance(mod_obj, griffe.Module):
            continue
        write_module_page(mod_qname, mod_obj, by_module[mod_qname], OUT_OVERVIEW)
    print(f"Generated {len(module_names)} module pages in {OUT_OVERVIEW}/")


if __name__ == "__main__":
    main()
