# `pymrm.convect.construct_convflux_bc`

```python
construct_convflux_bc(shape, x_f, x_c = None, bc = (None, None), v = 1.0, axis = 0, shapes_d = (None, None), format = 'csc')
```

Construct boundary-face upwind corrections and source terms.

**Parameters**

- **shape** : `tuple[int, ...]` — Cell-centered field shape.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates.
- **bc** : `tuple[dict | None, dict | None]` — Left and right boundary-condition dictionaries with keys ``a``, ``b``,
and ``d``.
- **v** : `float or array_like` — Face velocity field.
- **axis** : `int` — Convection axis.
- **shapes_d** : `tuple[tuple | None, tuple | None]` — Optional source-vector shapes for inhomogeneous boundary terms.
- **format** : `(csc, csr)` — Sparse format for returned operator matrices.

**Returns**

- `tuple` — ``(conv_matrix_bc, conv_bc)`` when ``shapes_d`` is not supplied, or
``(conv_matrix_left, conv_bc_left, conv_matrix_right, conv_bc_right)``
otherwise.
