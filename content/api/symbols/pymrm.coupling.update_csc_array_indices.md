# `pymrm.coupling.update_csc_array_indices`

## Signature

`pymrm.coupling.update_csc_array_indices(sparse_mat, shape, new_shape, offset=None)`

## Docstring

```text
Update CSC matrix row/column indexing for embedding in a larger domain.

.. deprecated::
   Use `update_array_indices` for automatic format dispatch.
```

## Implementation

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
