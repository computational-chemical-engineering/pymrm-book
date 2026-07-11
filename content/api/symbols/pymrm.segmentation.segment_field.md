# `pymrm.segmentation.segment_field`

[Back to module page](../modules/pymrm.segmentation) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`segment_field(values, seg, *, default = 0.0)`

## Summary

Expand per-segment values to a per-cell spatial field.

## Documentation

``lookup[seg.labels]`` — background cells (label 0) receive *default*.  For
example a per-particle diffusivity for the cell-centred-``D`` conjugate
diffusion pattern.

### Parameters

- `values` (*array_like or dict*)
  ``(n_segments, *trailing)`` array or ``{label: value}`` dict.

- `seg` (*Segmentation*)

- `default` (*optional*)
  Value for background (label 0) cells; ``0.0`` by default.

### Returns

- `ndarray, shape ``seg.labels.shape + trailing```

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L287-L308)

```python
def segment_field(values, seg, *, default=0.0):
    """Expand per-segment values to a per-cell spatial field.

    ``lookup[seg.labels]`` — background cells (label 0) receive *default*.  For
    example a per-particle diffusivity for the cell-centred-``D`` conjugate
    diffusion pattern.

    Parameters
    ----------
    values : array_like or dict
        ``(n_segments, *trailing)`` array or ``{label: value}`` dict.
    seg : Segmentation
    default : optional
        Value for background (label 0) cells; ``0.0`` by default.

    Returns
    -------
    ndarray, shape ``seg.labels.shape + trailing``
    """
    lookup, provided = _segment_lookup(values, seg.n_segments, default,
                                       "segment_field")
    return _index_lookup(lookup, provided, seg.labels, "segment_field")
```
