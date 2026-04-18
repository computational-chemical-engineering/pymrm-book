# `pymrm.coupling.construct_interface_matrices`

```python
construct_interface_matrices(shapes, x_fs, x_cs = (None, None), ic = ({'a': (1, 1), 'b': (0, 0), 'd': 0}, {'a': (0, 0), 'b': (1, -1), 'd': 0}), axis = 0, shapes_d = (None, None), format = 'csc')
```

Construct implicit interface-coupling matrices for two adjacent domains.

**Parameters**

- **shapes** : `tuple[tuple[int, ...], tuple[int, ...]]` — Shapes of the two subdomains.
- **x_fs** : `tuple[array_like, array_like]` — Face coordinates for each subdomain along ``axis``.
- **x_cs** : `tuple[array_like | None, array_like | None]` — Cell-center coordinates for each subdomain.
- **ic** : `tuple[dict, dict]` — Two interface equations. Each dictionary may define ``a``, ``b``, and
``d`` terms with coefficients for both subdomains.
- **axis** : `int` — Interface-normal axis.
- **shapes_d** : `tuple[tuple | None, tuple | None]` — Optional source-vector shapes for decomposed inhomogeneous terms.
- **format** : `(csc, csr)` — Sparse format for the homogeneous interface matrices.

**Returns**

- `tuple` — Without ``shapes_d``:
``(mat0, bc0, mat1, bc1)``.
With ``shapes_d``:
``(mat0, bc00, bc01, mat1, bc10, bc11)``.
