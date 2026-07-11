# `pymrm.segmentation.combine_interface_conditions`

[Back to module page](../modules/pymrm.segmentation) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`combine_interface_conditions(ic_by_segment, seg, ibm, *, default = None)`

## Summary

Merge per-segment interface conditions into one per-crossing ``ic``.

## Documentation

Each entry of ``ic_by_segment`` is a two-dict interface condition in the
format of `pymrm.apply_ibm_interface`.  The returned ``ic`` has, for
every coefficient slot, a per-crossing array assembled from the owning
segment of each crossing — so all crossings of one body share that body's
condition.

### Parameters

- `ic_by_segment` (*dict*)
  ``{label: ic}`` mapping segment label to a two-dict interface condition.
  Per-segment coefficients must be scalar or broadcastable to
  ``ibm.ns_shape`` (no nested per-crossing arrays).

- `seg` (*Segmentation*)

- `ibm` (*IBM*)

- `default` (*ic tuple, optional*)
  Interface condition for segments absent from ``ic_by_segment``.  If
  ``None`` a missing label that carries crossings raises ``ValueError``.

### Returns

- `tuple`
  A single ``ic`` usable with `pymrm.apply_ibm_interface` /
  `pymrm.construct_ibm_interface_values`.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L435-L482)

```python
def combine_interface_conditions(ic_by_segment, seg, ibm, *, default=None):
    """Merge per-segment interface conditions into one per-crossing ``ic``.

    Each entry of ``ic_by_segment`` is a two-dict interface condition in the
    format of :func:`pymrm.apply_ibm_interface`.  The returned ``ic`` has, for
    every coefficient slot, a per-crossing array assembled from the owning
    segment of each crossing — so all crossings of one body share that body's
    condition.

    Parameters
    ----------
    ic_by_segment : dict
        ``{label: ic}`` mapping segment label to a two-dict interface condition.
        Per-segment coefficients must be scalar or broadcastable to
        ``ibm.ns_shape`` (no nested per-crossing arrays).
    seg : Segmentation
    ibm : IBM
    default : ic tuple, optional
        Interface condition for segments absent from ``ic_by_segment``.  If
        ``None`` a missing label that carries crossings raises ``ValueError``.

    Returns
    -------
    tuple
        A single ``ic`` usable with :func:`pymrm.apply_ibm_interface` /
        :func:`pymrm.construct_ibm_interface_values`.
    """
    seg_ids = crossing_segments(seg, ibm)
    labels = sorted(int(k) for k in ic_by_segment)
    ns_ndim = len(ibm.ns_shape)

    def slot(eq, key, side):
        vals = {L: np.asarray(_ic_slot(ic_by_segment[L], eq, key, side),
                              dtype=float) for L in labels}
        dflt = (None if default is None
                else np.asarray(_ic_slot(default, eq, key, side), dtype=float))
        name = f"ic[{eq}]['{key}']" + ("" if side is None else f"[{side}]")
        lookup, provided = _segment_lookup(vals, seg.n_segments, dflt, name)
        picked = _index_lookup(lookup, provided, seg_ids, name)
        return _to_point_shape(picked, ns_ndim)

    ic0 = {"a": (slot(0, "a", 0), slot(0, "a", 1)),
           "b": (slot(0, "b", 0), slot(0, "b", 1)),
           "d": slot(0, "d", None)}
    ic1 = {"a": (slot(1, "a", 0), slot(1, "a", 1)),
           "b": (slot(1, "b", 0), slot(1, "b", 1)),
           "d": slot(1, "d", None)}
    return (ic0, ic1)
```
