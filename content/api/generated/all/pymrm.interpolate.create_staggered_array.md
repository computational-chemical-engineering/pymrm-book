# `pymrm.interpolate.create_staggered_array`

```python
create_staggered_array(array, shape, axis, x_f = None, x_c = None)
```

Create a face/staggered field from scalar, centered, or staggered input.

**Parameters**

- **array** : `array_like` — Input values. May be scalar, centered, or already staggered.
- **shape** : `tuple[int, ...] or int` — Target centered-field shape.
- **axis** : `int` — Staggering axis.
- **x_f** : `array_like` — Face and center coordinates used when centered input must be
interpolated to faces.
- **x_c** : `array_like` — Face and center coordinates used when centered input must be
interpolated to faces.

**Returns**

- `numpy.ndarray` — Broadcasted/interpolated array with staggered shape.
