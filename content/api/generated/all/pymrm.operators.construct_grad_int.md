# `pymrm.operators.construct_grad_int`

```python
construct_grad_int(shape, x_f, x_c = None, axis = 0, format = 'csc')
```

Construct the interior-face gradient operator.

**Parameters**

- **shape** : `tuple[int, ...]` — Cell-centered field shape.
- **x_f** : `array_like` — Face coordinates along ``axis``.
- **x_c** : `array_like` — Cell-center coordinates. If omitted, arithmetic midpoints are used.
- **axis** : `int` — Differentiation axis.
- **format** : `(csc, csr)` — Output sparse format.

**Returns**

- `scipy.sparse.csc_array or scipy.sparse.csr_array` — Matrix that maps cell-centered values to face-normal gradients.
