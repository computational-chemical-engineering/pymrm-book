# `pymrm.ibm.apply_ibm_vector`

[Back to module page](../modules/pymrm.ibm) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`apply_ibm_vector(vec, ibm)`

## Summary

Apply the IBM per-row conditioning scale to a flat vector.

## Documentation

When the operator matrix is constant it is modified once via
`apply_ibm`; any independent right-hand-side term must be scaled
by the same per-row factor to keep the system consistent.  This helper
applies the combined scale for both sides of the interface and expands
from the spatial grid to the full field.

### Parameters

- `vec` (*array_like*)
  Vector to scale, must have ``size == ibm.n_cells``.  May be shaped
  as the full field or passed as a flat array.

- `ibm` (*IBM*)
  Immersed-boundary data from `construct_ibm`.

### Returns

- `numpy.ndarray, shape (n_cells,)`
  Row-scaled vector, always returned as a 1-D flat array.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L1052-L1082)

```python
def apply_ibm_vector(vec, ibm):
    """Apply the IBM per-row conditioning scale to a flat vector.

    When the operator matrix is constant it is modified once via
    :func:`apply_ibm`; any independent right-hand-side term must be scaled
    by the same per-row factor to keep the system consistent.  This helper
    applies the combined scale for both sides of the interface and expands
    from the spatial grid to the full field.

    Parameters
    ----------
    vec : array_like
        Vector to scale, must have ``size == ibm.n_cells``.  May be shaped
        as the full field or passed as a flat array.
    ibm : IBM
        Immersed-boundary data from :func:`construct_ibm`.

    Returns
    -------
    numpy.ndarray, shape (n_cells,)
        Row-scaled vector, always returned as a 1-D flat array.
    """
    vec = np.asarray(vec, dtype=float).ravel()
    if vec.size != ibm.n_cells:
        raise ValueError(
            f"vec size {vec.size} != n_cells {ibm.n_cells}"
        )
    out = vec.copy()
    scale_rows, scale_vals = _combined_cut_scale(ibm)
    out[scale_rows] *= scale_vals
    return out
```
