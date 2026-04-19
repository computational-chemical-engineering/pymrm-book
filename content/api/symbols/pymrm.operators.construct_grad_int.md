# `pymrm.operators.construct_grad_int`

[Back to module page](../modules/pymrm.operators.md) · [Back to alphabetical overview](../alphabetical_overview.md)

## Signature

`construct_grad_int(shape, x_f, x_c = None, axis = 0, format = 'csc')`

## Summary

Construct the interior-face gradient operator.

## Documentation

### Parameters

- `shape` (*tuple[int, ...]*)
  Cell-centered field shape.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates. If omitted, arithmetic midpoints are used.

- `axis` (*int, optional*)
  Differentiation axis.

- `format` (*{'csc', 'csr'}, optional*)
  Output sparse format.

### Returns

- `scipy.sparse.csc_array or scipy.sparse.csr_array`
  Matrix that maps cell-centered values to face-normal gradients.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/operators.py#L68-L153)

```python
def construct_grad_int(shape, x_f, x_c=None, axis=0, format="csc"):
    """Construct the interior-face gradient operator.

    Parameters
    ----------
    shape : tuple[int, ...]
        Cell-centered field shape.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates. If omitted, arithmetic midpoints are used.
    axis : int, optional
        Differentiation axis.
    format : {'csc', 'csr'}, optional
        Output sparse format.

    Returns
    -------
    scipy.sparse.csc_array or scipy.sparse.csr_array
        Matrix that maps cell-centered values to face-normal gradients.
    """
    if axis < 0:
        axis += len(shape)
    shape_t = [
        math.prod(shape[:axis]),
        math.prod(shape[axis: axis + 1]),
        math.prod(shape[axis + 1:]),
    ]

    n0, n1, n2 = shape_t
    # Open grids for each dimension; the 4th axis selects the face-pair [j, j+1]
    i0 = np.arange(n0).reshape(-1, 1, 1, 1)
    i1 = np.arange(n1).reshape(1, -1, 1, 1)
    i2 = np.arange(n2).reshape(1, 1, -1, 1)
    face_pair = np.array([0, 1]).reshape(1, 1, 1, -1)
    i_f = np.ravel_multi_index((i0, i1 + face_pair, i2), (n0, n1 + 1, n2))

    if x_c is None:
        x_c = 0.5 * (x_f[:-1] + x_f[1:])

    dx_inv = np.tile(
        1 / (x_c[1:] - x_c[:-1]).reshape((1, -1, 1)), (n0, 1, n2)
    )
    values = np.empty(i_f.shape)
    values[:, 0, :, 0] = np.zeros((n0, n2))
    values[:, 1:, :, 0] = dx_inv
    values[:, :-1, :, 1] = -dx_inv
    values[:, -1, :, 1] = np.zeros((n0, n2))
    if format == "csc":
        grad_matrix = csc_array(
            (values.ravel(), i_f.ravel(), np.arange(0, i_f.size + 1, 2)),
            shape=(n0 * (n1 + 1) * n2, n0 * n1 * n2),
        )
    elif format == "csr":
        # Build CSR data in row (face) order with indptr.
        # Cell column indices: shape (n0, n1, n2)
        i_c = np.ravel_multi_index(
            (i0[..., 0], i1[..., 0], i2[..., 0]), (n0, n1, n2)
        )
        # Build (n0, n1+1, n2, 2) arrays: slot 0 = from cell j-1, slot 1 = from cell j
        csr_data = np.zeros((n0, n1 + 1, n2, 2))
        csr_cols = np.empty((n0, n1 + 1, n2, 2), dtype=np.intp)
        # Slot 0: right-side entry of cell j-1, contributes to face j (j=1..n1)
        csr_data[:, 1:, :, 0] = values[:, :, :, 1]
        csr_cols[:, 1:, :, 0] = i_c
        # Face 0 has no cell j-1; use cell 0's column so the dummy zero
        # entry lands on a valid column that already carries a zero value.
        csr_cols[:, 0, :, 0] = i_c[:, 0, :]
        # Slot 1: left-side entry of cell j, contributes to face j (j=0..n1-1)
        csr_data[:, :-1, :, 1] = values[:, :, :, 0]
        csr_cols[:, :-1, :, 1] = i_c
        # Face n1 has no cell j; use cell n1-1's column so the dummy zero
        # entry lands on a valid column that already carries a zero value.
        csr_cols[:, -1, :, 1] = i_c[:, -1, :]
        # Uniform 2 entries per row → simple indptr
        num_rows = n0 * (n1 + 1) * n2
        indptr = np.arange(0, 2 * num_rows + 1, 2, dtype=np.intp)
        grad_matrix = csr_array(
            (csr_data.ravel(), csr_cols.ravel(), indptr),
            shape=(n0 * (n1 + 1) * n2, n0 * n1 * n2),
        )
    else:
        raise ValueError(
            f"format must be 'csc' or 'csr', got {format!r}"
        )
    return grad_matrix
```
