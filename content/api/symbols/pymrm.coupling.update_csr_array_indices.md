# `pymrm.coupling.update_csr_array_indices`

[Back to module page](../modules/pymrm.coupling) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`update_csr_array_indices(sparse_mat, shape, new_shape, offset = None)`

## Summary

Update CSR matrix row/column indexing for embedding in a larger domain.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/coupling.py#L123-L161)

```python
def update_csr_array_indices(sparse_mat, shape, new_shape, offset=None):
    """Update CSR matrix row/column indexing for embedding in a larger domain."""
    shape, new_shape, offset = _parse_shape_offset(shape, new_shape, offset)

    # Extract matrix data and original indices
    data = sparse_mat.data
    col_indices = sparse_mat.indices    # Column indices
    row_pointers = sparse_mat.indptr    # Row pointers
    num_rows = sparse_mat.shape[0]
    num_cols = sparse_mat.shape[1]

    original_linear_cols = col_indices
    original_linear_rows = np.arange(num_rows)

    if (shape[1] is None) or (new_shape[1] is None):
        new_col_indices = original_linear_cols
    else:
        new_col_indices = translate_indices_to_larger_array(
            original_linear_cols, shape[1], new_shape[1], offset[1]
        )
        num_cols = math.prod(new_shape[1])

    if (shape[0] is None) or (new_shape[0] is None):
        new_row_pointers = row_pointers
    else:
        new_row_indices = translate_indices_to_larger_array(
            original_linear_rows, shape[0], new_shape[0], offset[0]
        )
        num_rows = math.prod(new_shape[0])
        new_row_pointers = np.zeros(num_rows + 1, dtype=int)
        new_row_pointers[new_row_indices + 1] = np.diff(row_pointers)
        new_row_pointers = np.cumsum(new_row_pointers)

    # Create a new sparse matrix with the corrected 2D shape
    updated_mat = csr_array(
        (data, new_col_indices, new_row_pointers), shape=(num_rows, num_cols)
    )

    return updated_mat
```
