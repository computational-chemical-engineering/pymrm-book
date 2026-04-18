# `pymrm.interpolate.interp_cntr_to_stagg`

```python
interp_cntr_to_stagg(cell_centered_values, x_f, x_c = None, axis = 0)
```

Interpolate cell-centered values to face/staggered locations.

**Parameters**

- **cell_centered_values** : `numpy.ndarray` — Values defined at cell centers.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates. If omitted, midpoint locations are used.
- **axis** : `int` — Interpolation axis.

**Returns**

- `numpy.ndarray` — Staggered values with one additional element along ``axis``.
