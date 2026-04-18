# `pymrm.grid.generate_grid`

```python
generate_grid(size, x_f = None, generate_x_c = False, x_c = None)
```

Return face coordinates and optionally cell-center coordinates.

**Parameters**

- **size** : `int` — Number of cells along the axis.
- **x_f** : `array_like` — Face coordinates. Accepted inputs are:

* ``None`` or an empty array: build a uniform grid on ``[0, 1]``;
* an array of length ``size + 1``: interpreted directly as face
  coordinates;
* an array-like of length ``2``: interpreted as ``(xmin, xmax)`` and
  used to build a uniform grid.
- **generate_x_c** : `bool` — If ``True``, also return cell-center coordinates.
- **x_c** : `array_like` — Explicit cell-center coordinates. When provided, length must equal
``size``.

**Returns**

- `numpy.ndarray or tuple[numpy.ndarray, numpy.ndarray]` — Face coordinates, and optionally cell-center coordinates.

**Raises**

- **ValueError** — If provided coordinates are inconsistent with ``size``.
