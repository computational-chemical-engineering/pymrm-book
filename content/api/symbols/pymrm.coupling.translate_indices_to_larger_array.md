# `pymrm.coupling.translate_indices_to_larger_array`

## Signature

`pymrm.coupling.translate_indices_to_larger_array(linear_indices, shape, new_shape, offset=None)`

## Docstring

```text
Map flat indices from a local array shape to a larger embedding shape.

Parameters
----------
linear_indices : array_like
    Flat indices defined in ``shape``.
shape : tuple[int, ...]
    Local array shape.
new_shape : tuple[int, ...]
    Embedding array shape.
offset : tuple[int, ...], optional
    Offset of the local array origin in the embedding array.

Returns
-------
numpy.ndarray
    Flat indices in ``new_shape``.
```

## Implementation

```python
def translate_indices_to_larger_array(linear_indices, shape, new_shape, offset=None):
    """Map flat indices from a local array shape to a larger embedding shape.

    Parameters
    ----------
    linear_indices : array_like
        Flat indices defined in ``shape``.
    shape : tuple[int, ...]
        Local array shape.
    new_shape : tuple[int, ...]
        Embedding array shape.
    offset : tuple[int, ...], optional
        Offset of the local array origin in the embedding array.

    Returns
    -------
    numpy.ndarray
        Flat indices in ``new_shape``.
    """

    # Convert linear indices to multi-indices based on the original subarray shape
    multi_indices = np.unravel_index(linear_indices, shape)

    # Shift multi-indices by the offset to their position in the larger array
    if offset is not None:
        adjusted_multi_indices = tuple(m + o for m, o in zip(multi_indices, offset))
    else:
        adjusted_multi_indices = multi_indices

    # Convert back to linear indices in the larger ND array
    new_linear_indices = np.ravel_multi_index(adjusted_multi_indices, new_shape)

    return new_linear_indices

```
