# `pymrm.segmentation.wall_patch`

[Back to module page](../modules/pymrm.segmentation) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`wall_patch(seg, ibm, axis, side)`

## Summary

Segment labels on one domain wall, shaped as a full-field coefficient.

## Documentation

### Parameters

- `seg` (*Segmentation*)

- `ibm` (*IBM*)

- `axis` (*int*)
  Full-field axis of the wall (must be one of ``ibm.axes``), matching the
  ``axis`` argument of the boundary-condition operators.

- `side` (*{'lower', 'upper'}*)
  Which end of that axis, matching the ``(bc_lower, bc_upper)`` tuple.

### Returns

- `ndarray of int`
  Label of the boundary cell (``0`` = other region) reshaped to full field
  rank with the wall ``axis`` and every non-spatial axis at size 1.  Use
  directly in ``np.where`` to build a ``{a, b, d}`` wall coefficient, e.g.
  ``np.where(wall_patch(seg, ibm, 0, "lower") == k, value_k, other)``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L352-L379)

```python
def wall_patch(seg, ibm, axis, side):
    """Segment labels on one domain wall, shaped as a full-field coefficient.

    Parameters
    ----------
    seg : Segmentation
    ibm : IBM
    axis : int
        Full-field axis of the wall (must be one of ``ibm.axes``), matching the
        ``axis`` argument of the boundary-condition operators.
    side : {'lower', 'upper'}
        Which end of that axis, matching the ``(bc_lower, bc_upper)`` tuple.

    Returns
    -------
    ndarray of int
        Label of the boundary cell (``0`` = other region) reshaped to full field
        rank with the wall ``axis`` and every non-spatial axis at size 1.  Use
        directly in ``np.where`` to build a ``{a, b, d}`` wall coefficient, e.g.
        ``np.where(wall_patch(seg, ibm, 0, "lower") == k, value_k, other)``.
    """
    _check_spatial_match(seg, ibm)
    sax, layer = _spatial_axis(ibm, axis, side)
    face = np.take(seg.labels, layer, axis=sax)
    full_shape = tuple(
        ibm.shape[a] if (a in tuple(ibm.axes) and a != axis) else 1
        for a in range(len(ibm.shape)))
    return face.reshape(full_shape).astype(np.intp)
```
