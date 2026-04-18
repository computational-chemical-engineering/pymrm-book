# `pymrm.grid.non_uniform_grid`

```python
non_uniform_grid(left_bound, right_bound, num_points, dx_inf, factor)
```

Generate a one-dimensional stretched face grid.

**Parameters**

- **left_bound** : `float` — Domain bounds.
- **right_bound** : `float` — Domain bounds.
- **num_points** : `int` — Number of returned face coordinates, including both boundaries.
- **dx_inf** : `float` — Asymptotic cell width used in the stretching expression.
- **factor** : `float` — Geometric stretching factor. Values larger than ``1`` stretch cells;
values between ``0`` and ``1`` compress cells.

**Returns**

- `numpy.ndarray` — Monotonic array of face coordinates with length ``num_points``.
