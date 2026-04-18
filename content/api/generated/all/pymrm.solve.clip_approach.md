# `pymrm.solve.clip_approach`

```python
clip_approach(values, dummy, lower_bounds = 0, upper_bounds = None, factor = 0)
```

Project values onto bounds, optionally with a relaxed approach rule.

**Parameters**

- **values** : `numpy.ndarray` — Values to modify in place.
- **dummy** : `Any` — Placeholder argument kept for API compatibility.
- **lower_bounds** : `float or numpy.ndarray` — Lower and upper bounds. Scalars and broadcastable arrays are supported.
- **upper_bounds** : `float or numpy.ndarray` — Lower and upper bounds. Scalars and broadcastable arrays are supported.
- **factor** : `float` — Relaxation factor for out-of-bound entries. ``0`` applies strict clipping.
Non-zero values apply a linear approach update toward the violated bound.
