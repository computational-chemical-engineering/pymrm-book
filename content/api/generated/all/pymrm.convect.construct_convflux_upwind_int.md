# `pymrm.convect.construct_convflux_upwind_int`

```python
construct_convflux_upwind_int(shape, v = 1.0, axis = 0, format = 'csc')
```

Construct the internal-face upwind advection operator.

**Parameters**

- **shape** : `tuple[int, ...]` — Cell-centered field shape.
- **v** : `float or array_like` — Face velocity field.
- **axis** : `int` — Convection axis.
- **format** : `(csc, csr)` — Sparse format of the returned matrix.

**Returns**

- `scipy.sparse.csc_array or scipy.sparse.csr_array` — Sparse matrix mapping cell-centered values to interior face fluxes.
