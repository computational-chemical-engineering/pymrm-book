# `pymrm.helpers.describe_bc`

[Back to module page](../modules/pymrm.helpers) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`describe_bc(bc, x_f = None, axis_name = 'x', var = 'c')`

## Summary

Describe boundary-condition dictionaries as the equations they impose.

## Documentation

pymrm boundary conditions read ``a * dc/dn + b * c = d`` with ``n`` the
OUTWARD normal, so the same dictionary means opposite gradients at the two
ends. This helper writes each condition out in terms of the axis direction,
which makes sign errors visible.

### Parameters

- `bc` (*tuple[dict | None, dict | None]*)
  Lower and upper boundary dictionaries with keys ``a``, ``b``, ``d``.

- `x_f` (*array_like, optional*)
  Face coordinates along the axis; used to print the boundary positions.

- `axis_name` (*str, optional*)
  Name of the coordinate (default ``"x"``).

- `var` (*str, optional*)
  Name of the field (default ``"c"``).

### Returns

- `str`
  One line per boundary, for example
  ``lower (x=0, outward normal -x): -1*dc/dx + 0*c = 2  [Neumann]``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/helpers.py#L227-L269)

```python
def describe_bc(bc, x_f=None, axis_name="x", var="c"):
    """Describe boundary-condition dictionaries as the equations they impose.

    pymrm boundary conditions read ``a * dc/dn + b * c = d`` with ``n`` the
    OUTWARD normal, so the same dictionary means opposite gradients at the two
    ends. This helper writes each condition out in terms of the axis direction,
    which makes sign errors visible.

    Parameters
    ----------
    bc : tuple[dict | None, dict | None]
        Lower and upper boundary dictionaries with keys ``a``, ``b``, ``d``.
    x_f : array_like, optional
        Face coordinates along the axis; used to print the boundary positions.
    axis_name : str, optional
        Name of the coordinate (default ``"x"``).
    var : str, optional
        Name of the field (default ``"c"``).

    Returns
    -------
    str
        One line per boundary, for example
        ``lower (x=0, outward normal -x): -1*dc/dx + 0*c = 2  [Neumann]``.
    """
    lines = []
    for side, sign, index in (("lower", "-", 0), ("upper", "+", -1)):
        entry = bc[index] if bc is not None else None
        where = f"{axis_name}={float(np.asarray(x_f)[index]):.6g}, " if x_f is not None else ""
        head = f"{side} ({where}outward normal {sign}{axis_name})"
        if entry is None:
            lines.append(f"{head}: None, treated as a = b = d = 0")
            continue
        if is_outflow_bc(entry):
            lines.append(f"{head}: outflow, face value = adjacent cell value, zero diffusive flux")
            continue
        a, b, d = (entry.get(key, 0.0) for key in ("a", "b", "d"))
        a_text = _format_coefficient(np.asarray(a, dtype=float) * (-1.0 if sign == "-" else 1.0) + 0.0)
        lines.append(
            f"{head}: {a_text}*d{var}/d{axis_name} + {_format_coefficient(b)}*{var} = "
            f"{_format_coefficient(d)}  [{_classify_bc(a, b)}]"
        )
    return "\n".join(lines)
```
