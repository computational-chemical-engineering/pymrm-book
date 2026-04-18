# `pymrm.convect.construct_convflux_upwind`

```python
construct_convflux_upwind(shape, x_f, x_c = None, bc = (None, None), v = 1.0, axis = 0, shapes_d = (None, None), format = 'csc')
```

Construct a first-order upwind convective-flux operator.

**Parameters**

- **shape** : `tuple[int, ...] or int` — Cell-centered field shape.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates. If omitted, arithmetic midpoints are used.
- **bc** : `tuple[dict | None, dict | None]` — Left and right boundary-condition dictionaries with keys ``a``, ``b``,
and ``d``.
- **v** : `float or array_like` — Face velocity field. Scalars and broadcastable arrays are accepted.
- **axis** : `int` — Convection axis.
- **shapes_d** : `tuple[tuple | None, tuple | None]` — Optional source-vector shapes for boundary inhomogeneities.
- **format** : `(csc, csr)` — Sparse format for returned operator matrices.

**Returns**

- `tuple` — Without ``shapes_d``: ``(conv_matrix, conv_bc)``.
With ``shapes_d``: ``(conv_matrix, conv_bc_left, conv_bc_right)``.
