# `pymrm.coupling.update_array_indices`

## Signature

`pymrm.coupling.update_array_indices(sparse_mat, shape, new_shape, offset=None)`

## Docstring

```text
Update sparse-matrix indices for a new embedding shape.

Parameters
----------
sparse_mat : scipy.sparse.sparray
    Input matrix. CSR and CSC are supported.
shape, new_shape : tuple or tuple[tuple, tuple]
    Original and target logical shapes for rows and columns. A single tuple
    applies to both rows and columns.
offset : tuple or tuple[tuple, tuple], optional
    Optional row/column offsets of the local block in the larger domain.

Returns
-------
scipy.sparse.sparray
    Matrix with updated shape and indices, preserving the input format where
    possible.
```

## Implementation

```python
def update_array_indices(sparse_mat, shape, new_shape, offset=None):
    """Update sparse-matrix indices for a new embedding shape.

    Parameters
    ----------
    sparse_mat : scipy.sparse.sparray
        Input matrix. CSR and CSC are supported.
    shape, new_shape : tuple or tuple[tuple, tuple]
        Original and target logical shapes for rows and columns. A single tuple
        applies to both rows and columns.
    offset : tuple or tuple[tuple, tuple], optional
        Optional row/column offsets of the local block in the larger domain.

    Returns
    -------
    scipy.sparse.sparray
        Matrix with updated shape and indices, preserving the input format where
        possible.
    """
    if isinstance(sparse_mat, csr_array):
        return update_csr_array_indices(sparse_mat, shape, new_shape, offset)
    # Default: convert to CSC if needed, then update
    sparse_mat = csc_array(sparse_mat)
    return _update_csc_array_indices(sparse_mat, shape, new_shape, offset)

```
