# `pymrm.segmentation.wall_contact`

[Back to module page](../modules/pymrm.segmentation) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`wall_contact(seg)`

## Summary

Whether each segment reaches each domain wall.

## Documentation

### Returns

- `ndarray of bool, shape (n_segments, ndim_spatial, 2)`
  ``out[s - 1, a, 0]`` / ``out[s - 1, a, 1]`` is ``True`` when segment
  ``s`` has cells in the first / last layer along spatial axis ``a``.

### Notes

A fluid-side segmentation (``region="positive"``) whose segment touches no
wall is an isolated pocket; with all-Neumann surroundings it makes the
operator singular.  Detect them with
``np.flatnonzero(~wall_contact(seg).any(axis=(1, 2))) + 1``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L315-L339)

```python
def wall_contact(seg):
    """Whether each segment reaches each domain wall.

    Returns
    -------
    ndarray of bool, shape (n_segments, ndim_spatial, 2)
        ``out[s - 1, a, 0]`` / ``out[s - 1, a, 1]`` is ``True`` when segment
        ``s`` has cells in the first / last layer along spatial axis ``a``.

    Notes
    -----
    A fluid-side segmentation (``region="positive"``) whose segment touches no
    wall is an isolated pocket; with all-Neumann surroundings it makes the
    operator singular.  Detect them with
    ``np.flatnonzero(~wall_contact(seg).any(axis=(1, 2))) + 1``.
    """
    labels = seg.labels
    out = np.zeros((seg.n_segments, labels.ndim, 2), dtype=bool)
    for a in range(labels.ndim):
        for si, layer in enumerate((0, -1)):
            face = np.take(labels, layer, axis=a)
            present = np.unique(face)
            present = present[present > 0]
            out[present - 1, a, si] = True
    return out
```
