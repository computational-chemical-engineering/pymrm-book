# `pymrm.operators.construct_grad`

```python
construct_grad(shape, x_f, x_c = None, bc = (None, None), axis = 0, shapes_d = (None, None), format = 'csc')
```

Construct the full gradient operator including boundary contributions.

**Parameters**

- **shape** : `tuple[int, ...] or int` — Cell-centered field shape.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates along ``axis``. If omitted, they are generated
as arithmetic midpoints.
- **bc** : `tuple[dict | None, dict | None]` — Left and right boundary-condition dictionaries with coefficients
``'a'``, ``'b'``, and ``'d'``.
- **axis** : `int` — Differentiation axis.
- **shapes_d** : `tuple[tuple | None, tuple | None]` — Optional output shapes for inhomogeneous boundary source vectors.
- **format** : `(csc, csr)` — Sparse format used for returned operator matrices.

**Returns**

- `tuple` — Without ``shapes_d``: ``(grad_matrix, grad_bc)``.
With ``shapes_d``: ``(grad_matrix, grad_bc_left, grad_bc_right)``.
