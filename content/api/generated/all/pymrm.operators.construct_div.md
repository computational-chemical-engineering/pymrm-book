# `pymrm.operators.construct_div`

```python
construct_div(shape, x_f, nu = 0, axis = 0, format = 'csc')
```

Construct a divergence matrix that maps face fluxes to cell balances.

**Parameters**

- **shape** : `tuple[int, ...] or int` — Cell-centered field shape.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **nu** : `int or callable` — Geometry descriptor. ``0`` gives Cartesian, ``1`` cylindrical,
``2`` spherical, and a callable ``nu(x)`` enables custom metrics.
- **axis** : `int` — Axis for flux divergence.
- **format** : `(csc, csr)` — Sparse format of the returned operator.

**Returns**

- `scipy.sparse.csc_array or scipy.sparse.csr_array` — Divergence operator.
