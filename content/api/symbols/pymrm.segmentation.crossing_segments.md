# `pymrm.segmentation.crossing_segments`

[Back to module page](../modules/pymrm.segmentation) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`crossing_segments(seg, ibm)`

## Summary

Segment label of the body bounded by each IBM crossing.

## Documentation

For ``region="negative"`` the label of the *inside* (solid) cut cell is
returned; for ``region="positive"`` the *outside* (fluid) cut cell.  In
either case the cut cell lies in the segmented region, so every returned
label is in ``1 .. n_segments``.

### Parameters

- `seg` (*Segmentation*)

- `ibm` (*IBM*)

### Returns

- `ndarray of int, shape (n_crossings,)`

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L142-L169)

```python
def crossing_segments(seg, ibm):
    """Segment label of the body bounded by each IBM crossing.

    For ``region="negative"`` the label of the *inside* (solid) cut cell is
    returned; for ``region="positive"`` the *outside* (fluid) cut cell.  In
    either case the cut cell lies in the segmented region, so every returned
    label is in ``1 .. n_segments``.

    Parameters
    ----------
    seg : Segmentation
    ibm : IBM

    Returns
    -------
    ndarray of int, shape (n_crossings,)
    """
    _check_spatial_match(seg, ibm)
    if ibm.n_crossings == 0:
        return np.empty(0, dtype=np.intp)
    rows = ibm.row_in if seg.region == "negative" else ibm.row_out
    out = seg.labels.ravel()[rows].astype(np.intp)
    if np.any(out == 0):
        raise RuntimeError(
            "a crossing mapped to background label 0; this should not happen "
            "for a segmentation of the same side as the crossings — please "
            "report")
    return out
```
