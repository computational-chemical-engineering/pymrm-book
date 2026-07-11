# `pymrm.segmentation.segment_values`

[Back to module page](../modules/pymrm.segmentation) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`segment_values(values, seg, ibm, *, default = None)`

## Summary

Expand per-segment values to a per-crossing array for `pymrm.apply_ibm`.

## Documentation

### Parameters

- `values` (*array_like or dict*)
  Either an array of shape ``(n_segments, *trailing)`` or a
  ``{label: value}`` dict.  The trailing dimensions must be broadcastable
  to ``ibm.ns_shape`` (the non-spatial axes).

- `seg` (*Segmentation*)

- `ibm` (*IBM*)

- `default` (*optional*)
  Value for segments absent from a ``dict`` input.  If ``None`` a missing
  label that carries crossings raises ``ValueError``.

### Returns

- `ndarray, shape ``(n_crossings, 1, ..., 1, *trailing)```
  Canonical point-value array, ready to pass as ``values_outside`` /
  ``values_inside``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L259-L284)

```python
def segment_values(values, seg, ibm, *, default=None):
    """Expand per-segment values to a per-crossing array for :func:`pymrm.apply_ibm`.

    Parameters
    ----------
    values : array_like or dict
        Either an array of shape ``(n_segments, *trailing)`` or a
        ``{label: value}`` dict.  The trailing dimensions must be broadcastable
        to ``ibm.ns_shape`` (the non-spatial axes).
    seg : Segmentation
    ibm : IBM
    default : optional
        Value for segments absent from a ``dict`` input.  If ``None`` a missing
        label that carries crossings raises ``ValueError``.

    Returns
    -------
    ndarray, shape ``(n_crossings, 1, ..., 1, *trailing)``
        Canonical point-value array, ready to pass as ``values_outside`` /
        ``values_inside``.
    """
    seg_ids = crossing_segments(seg, ibm)
    lookup, provided = _segment_lookup(values, seg.n_segments, default,
                                       "segment_values")
    picked = _index_lookup(lookup, provided, seg_ids, "segment_values")
    return _to_point_shape(picked, len(ibm.ns_shape))
```
