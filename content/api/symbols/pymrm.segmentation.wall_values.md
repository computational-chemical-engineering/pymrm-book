# `pymrm.segmentation.wall_values`

[Back to module page](../modules/pymrm.segmentation) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`wall_values(values, seg, ibm, axis, side, *, default = 0.0)`

## Summary

Per-segment values on one domain wall as a full-field BC coefficient.

## Documentation

Combines `wall_patch` with a per-segment lookup so that a
wall-touching body can be given the same condition on its wall patch as on
its immersed boundary.  The per-segment values may carry non-spatial
structure (broadcastable to ``ibm.ns_shape``).

### Parameters

- `values` (*array_like or dict*)
  ``(n_segments, *trailing)`` array or ``{label: value}`` dict, trailing
  broadcastable to ``ibm.ns_shape``.

- `seg, ibm, axis, side` (*see `wall_patch`.*)

- `default` (*optional*)
  Value for cells not in the segmented region (label 0); ``0.0`` default.

### Returns

- `ndarray`
  Full field shape with the wall ``axis`` at size 1 — a ready ``a`` / ``b``
  / ``d`` coefficient for `pymrm.construct_grad` and friends.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L382-L419)

```python
def wall_values(values, seg, ibm, axis, side, *, default=0.0):
    """Per-segment values on one domain wall as a full-field BC coefficient.

    Combines :func:`wall_patch` with a per-segment lookup so that a
    wall-touching body can be given the same condition on its wall patch as on
    its immersed boundary.  The per-segment values may carry non-spatial
    structure (broadcastable to ``ibm.ns_shape``).

    Parameters
    ----------
    values : array_like or dict
        ``(n_segments, *trailing)`` array or ``{label: value}`` dict, trailing
        broadcastable to ``ibm.ns_shape``.
    seg, ibm, axis, side : see :func:`wall_patch`.
    default : optional
        Value for cells not in the segmented region (label 0); ``0.0`` default.

    Returns
    -------
    ndarray
        Full field shape with the wall ``axis`` at size 1 — a ready ``a`` / ``b``
        / ``d`` coefficient for :func:`pymrm.construct_grad` and friends.
    """
    _check_spatial_match(seg, ibm)
    sax, layer = _spatial_axis(ibm, axis, side)
    face = np.take(seg.labels, layer, axis=sax)
    lookup, provided = _segment_lookup(values, seg.n_segments, default,
                                       "wall_values",
                                       trailing_shape=ibm.ns_shape)
    picked = _index_lookup(lookup, provided, face, "wall_values")

    # picked axes: [other spatial (ascending full-axis order), *ns_shape].
    # Reinsert the reduced spatial axis, then move to interleaved field order.
    spatial_sorted = sorted(ibm.axes)
    ns_sorted = [a for a in range(len(ibm.shape)) if a not in tuple(ibm.axes)]
    grouped = np.expand_dims(picked, spatial_sorted.index(axis))
    dest = spatial_sorted + ns_sorted
    return np.moveaxis(grouped, range(grouped.ndim), dest)
```
