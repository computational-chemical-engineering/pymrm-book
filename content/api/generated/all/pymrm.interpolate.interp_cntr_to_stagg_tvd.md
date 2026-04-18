# `pymrm.interpolate.interp_cntr_to_stagg_tvd`

```python
interp_cntr_to_stagg_tvd(cell_centered_values, x_f, x_c = None, bc = None, v = 0, tvd_limiter = None, axis = 0)
```

Perform TVD interpolation from cell centers to faces.

**Parameters**

- **cell_centered_values** : `numpy.ndarray` — Cell-centered values.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates. If omitted, midpoint locations are used.
- **bc** : `tuple[dict | None, dict | None]` — Left and right boundary-condition dictionaries with keys ``a``, ``b``,
and ``d``.
- **v** : `float or array_like` — Face velocity used to determine upwind/downwind directions.
- **tvd_limiter** : `callable` — Limiter function with signature ``phi(c_norm, x_norm_c, x_norm_d)``. If
``None``, the routine returns linear upwind interpolation without TVD
correction.
- **axis** : `int` — Interpolation axis.

**Returns**

- `tuple[numpy.ndarray, numpy.ndarray]` — Interpolated staggered values and TVD correction term.
