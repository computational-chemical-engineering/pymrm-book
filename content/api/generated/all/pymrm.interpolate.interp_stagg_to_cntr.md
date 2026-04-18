# `pymrm.interpolate.interp_stagg_to_cntr`

```python
interp_stagg_to_cntr(staggered_values, x_f, x_c = None, axis = 0)
```

Interpolate face/staggered values to cell centers.

**Parameters**

- **staggered_values** : `numpy.ndarray` — Values defined on staggered (face) locations.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates. If omitted, midpoint interpolation is used.
- **axis** : `int` — Interpolation axis.

**Returns**

- `numpy.ndarray` — Cell-centered values with one fewer element along ``axis``.
