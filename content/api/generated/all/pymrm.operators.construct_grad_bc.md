# `pymrm.operators.construct_grad_bc`

```python
construct_grad_bc(shape, x_f, x_c = None, bc = (None, None), axis = 0, shapes_d = (None, None), format = 'csc')
```

Construct boundary-face gradient corrections and source terms.

**Parameters**

- **shape** : `tuple[int, ...]` — Cell-centered field shape.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates.
- **bc** : `tuple[dict | None, dict | None]` — Left and right boundary-condition dictionaries with keys ``a``, ``b``,
and ``d``.
- **axis** : `int` — Differentiation axis.
- **shapes_d** : `tuple[tuple | None, tuple | None]` — Optional source-vector shapes for left/right boundary contributions.
- **format** : `(csc, csr)` — Sparse format for returned operator matrices.

**Returns**

- `tuple` — ``(grad_matrix_bc, grad_bc)`` when ``shapes_d`` is not supplied, or
``(grad_matrix_left, grad_bc_left, grad_matrix_right, grad_bc_right)``
otherwise.
