# `pymrm.convect.construct_convflux_upwind_int`

## Signature

`pymrm.convect.construct_convflux_upwind_int(shape, v=1.0, axis=0, format='csc')`

## Docstring

```text
Construct the internal-face upwind advection operator.

Parameters
----------
shape : tuple[int, ...]
    Cell-centered field shape.
v : float or array_like, optional
    Face velocity field.
axis : int, optional
    Convection axis.
format : {'csc', 'csr'}, optional
    Sparse format of the returned matrix.

Returns
-------
scipy.sparse.csc_array or scipy.sparse.csr_array
    Sparse matrix mapping cell-centered values to interior face fluxes.
```

## Implementation

```python
def construct_convflux_upwind_int(shape, v=1.0, axis=0, format="csc"):
    """Construct the internal-face upwind advection operator.

    Parameters
    ----------
    shape : tuple[int, ...]
        Cell-centered field shape.
    v : float or array_like, optional
        Face velocity field.
    axis : int, optional
        Convection axis.
    format : {'csc', 'csr'}, optional
        Sparse format of the returned matrix.

    Returns
    -------
    scipy.sparse.csc_array or scipy.sparse.csr_array
        Sparse matrix mapping cell-centered values to interior face fluxes.
    """
    shape_f = shape[:axis] + (shape[axis] + 1,) + shape[axis + 1:]
    shape_t = (math.prod(shape[:axis]), shape[axis], math.prod(shape[axis + 1:]))
    shape_f_t = (shape_t[0], shape_f[axis], shape_t[2])

    n0, n1, n2 = shape_t
    if isinstance(v, (float, int)):
        v_t = np.broadcast_to(np.array(v), shape_f_t)
    else:
        v_t = v.reshape(shape_f_t)
    fltr_v_pos = v_t > 0
    # Internal faces: indices 1 .. n1-1 along the axis
    i0 = np.arange(n0).reshape(-1, 1, 1)
    i1_int = np.arange(1, n1).reshape(1, -1, 1)
    i2 = np.arange(n2).reshape(1, 1, -1)
    i_f = np.ravel_multi_index((i0, i1_int, i2), shape_f_t)
    # Upwind: shift cell index left by 1 when velocity is positive
    i_c = np.ravel_multi_index((i0, i1_int - fltr_v_pos[:, 1:-1, :], i2), shape_t)
    if format == "csc":
        conv_matrix = csc_array(
            (v_t[:, 1:-1, :].ravel(), (i_f.ravel(), i_c.ravel())),
            shape=(math.prod(shape_f_t), math.prod(shape_t)),
        )
    elif format == "csr":
        # Each internal face (j=1..n1-1) has 1 entry; boundary faces have 0.
        nnz_per_face = np.zeros(n1 + 1, dtype=np.intp)
        nnz_per_face[1:n1] = 1
        row_nnz = np.tile(np.repeat(nnz_per_face, n2), n0)
        indptr = np.zeros(n0 * (n1 + 1) * n2 + 1, dtype=np.intp)
        np.cumsum(row_nnz, out=indptr[1:])
        conv_matrix = csr_array(
            (v_t[:, 1:-1, :].ravel(), i_c.ravel(), indptr),
            shape=(math.prod(shape_f_t), math.prod(shape_t)),
        )
    else:
        raise ValueError(
            f"format must be 'csc' or 'csr', got {format!r}"
        )
    conv_matrix.sort_indices()
    return conv_matrix

```
