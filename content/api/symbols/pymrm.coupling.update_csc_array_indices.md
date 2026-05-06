# `pymrm.coupling.update_csc_array_indices`

[Back to module page](../modules/pymrm.coupling) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`update_csc_array_indices(sparse_mat, shape, new_shape, offset = None)`

## Summary

Update CSC matrix row/column indexing for embedding in a larger domain.

## Documentation

.. deprecated::
   Use `update_array_indices` for automatic format dispatch.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/89c91222a061c475e309f0ea6a6207ac8d5a3d20/src/pymrm/coupling.py#L67-L78)

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
