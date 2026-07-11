# `pymrm.segmentation.segment_domain`

[Back to module page](../modules/pymrm.segmentation) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`segment_domain(sdf, *, region = 'negative', connectivity = 1)`

## Summary

Label the disjoint regions of a signed distance field.

## Documentation

### Parameters

- `sdf` (*array_like*)
  Signed distance field sampled at the spatial cell centres, as passed to
  `pymrm.construct_ibm`.

- `region` (*{'negative', 'positive'}, optional*)
  Segment ``sdf < 0`` (solid bodies, default) or ``sdf >= 0`` (fluid
  regions).

- `connectivity` (*int, optional*)
  Neighbour connectivity for labelling, ``1 <= connectivity <= sdf.ndim``.
  ``1`` (default) links face neighbours only, matching the staircase
  boundary of the IBM crossings; ``sdf.ndim`` also links diagonal
  neighbours.

### Returns

- `Segmentation`

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L88-L128)

```python
def segment_domain(sdf, *, region="negative", connectivity=1):
    """Label the disjoint regions of a signed distance field.

    Parameters
    ----------
    sdf : array_like
        Signed distance field sampled at the spatial cell centres, as passed to
        :func:`pymrm.construct_ibm`.
    region : {'negative', 'positive'}, optional
        Segment ``sdf < 0`` (solid bodies, default) or ``sdf >= 0`` (fluid
        regions).
    connectivity : int, optional
        Neighbour connectivity for labelling, ``1 <= connectivity <= sdf.ndim``.
        ``1`` (default) links face neighbours only, matching the staircase
        boundary of the IBM crossings; ``sdf.ndim`` also links diagonal
        neighbours.

    Returns
    -------
    Segmentation
    """
    sdf = np.asarray(sdf)
    if sdf.ndim == 0:
        raise ValueError("sdf must be an array with at least one spatial axis")
    if region == "negative":
        mask = sdf < 0.0
    elif region == "positive":
        mask = ~(sdf < 0.0)
    else:
        raise ValueError(
            f"region must be 'negative' or 'positive', got {region!r}")
    if not 1 <= connectivity <= sdf.ndim:
        raise ValueError(
            f"connectivity must be in 1..{sdf.ndim}, got {connectivity}")

    structure = generate_binary_structure(sdf.ndim, connectivity)
    labels, n = _ndimage_label(mask, structure=structure)
    sizes = np.bincount(labels.ravel(),
                        minlength=n + 1)[1:].astype(np.intp)
    return Segmentation(labels=labels, n_segments=int(n), region=region,
                        connectivity=int(connectivity), sizes=sizes)
```
