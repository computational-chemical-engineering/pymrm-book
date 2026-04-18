# `pymrm.interpolate.compute_boundary_values`

```python
compute_boundary_values(cell_centered_values, x_f, x_c = None, bc = None, axis = 0, bound_id = None)
```

Compute boundary values and boundary-normal gradients.

**Parameters**

- **cell_centered_values** : `numpy.ndarray` — Cell-centered solution values.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates.
- **bc** : `dict or tuple[dict | None, dict | None]` — Boundary-condition data. For a single boundary query (``bound_id`` set),
a single dictionary is accepted. For both boundaries, pass a
two-element tuple.
- **axis** : `int` — Axis normal to the boundary.
- **bound_id** : `(0, 1)` — Boundary selector. ``None`` returns both boundaries.

**Returns**

- `tuple` — If ``bound_id`` is ``None``:
``(value_left, grad_left, value_right, grad_right)``.
Otherwise: ``(value, grad)`` for the requested boundary.
