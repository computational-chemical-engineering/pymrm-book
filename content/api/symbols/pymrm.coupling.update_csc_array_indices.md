# `pymrm.coupling.update_csc_array_indices`

[Back to module page](../modules/pymrm.coupling.md) · [Back to alphabetical overview](../alphabetical_overview.md)

## Signature

`update_csc_array_indices(sparse_mat, shape, new_shape, offset = None)`

## Summary

Update CSC matrix row/column indexing for embedding in a larger domain.

## Documentation

.. deprecated::
   Use `update_array_indices` for automatic format dispatch.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/coupling.py#L67-L78)

```python
def update_csc_array_indices(sparse_mat, shape, new_shape, offset=None):
    """Update CSC matrix row/column indexing for embedding in a larger domain.

    .. deprecated::
       Use :func:`update_array_indices` for automatic format dispatch.
    """
    warnings.warn(
        "update_csc_array_indices is deprecated. Use update_array_indices instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _update_csc_array_indices(sparse_mat, shape, new_shape, offset)
```
