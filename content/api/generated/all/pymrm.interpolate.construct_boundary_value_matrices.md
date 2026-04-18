# `pymrm.interpolate.construct_boundary_value_matrices`

```python
construct_boundary_value_matrices(shape, x_f, x_c = None, bc = None, axis = 0, bound_id = 0, shape_d = None, format = 'csc')
```

Build matrices that evaluate boundary values from cell-centered unknowns.

**Parameters**

- **shape** : `tuple[int, ...]` — Cell-centered field shape.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates near the selected boundary.
- **bc** : `dict` — Boundary-condition dictionary with keys ``a``, ``b``, and ``d``.
- **axis** : `int` — Boundary-normal axis.
- **bound_id** : `(0, 1)` — ``0`` for the lower/left boundary, ``1`` for upper/right.
- **shape_d** : `tuple[int, ...]` — Shape of external inhomogeneous source unknowns.
- **format** : `(csc, csr)` — Sparse format for the homogeneous matrix.

**Returns**

- `tuple` — ``(matrix, mat_bc)`` where ``matrix`` maps cell-centered values to
boundary values and ``mat_bc`` maps inhomogeneous boundary terms.
