# `pymrm.segmentation.Segmentation`

[Back to module page](../modules/pymrm.segmentation) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`Segmentation()`

## Summary

Per-cell integer labelling of one region of the spatial grid.

## Documentation

Produced by `segment_domain` (connected components of a signed
distance field) or by `pymrm.construct_ibm_particles` (one label per
particle, which keeps touching particles distinct).  The per-segment
helpers (`crossing_segments`, `segment_values`,
`combine_interface_conditions`, `wall_patch`,
`wall_values`, `segment_field`) work with either source.

### Attributes

- `labels` (*ndarray of int*)
  Integer label field with the shape of the spatial grid.  ``0`` marks
  the *other* region; the labelled region carries ``1 .. n_segments``.

- `n_segments` (*int*)
  Number of disjoint segments.

- `region` (*{'negative', 'positive'}*)
  Which side of the interface was labelled (``sdf < 0`` or ``sdf >= 0``).

- `connectivity` (*int*)
  Connectivity used for labelling (``1`` = faces, ``labels.ndim`` =
  including diagonals).  Reported as ``1`` for the particle path.

- `sizes` (*ndarray of int, shape (n_segments,)*)
  Number of cells in each segment; ``sizes[s - 1]`` is the size of the
  segment with label ``s``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/segmentation.py#L54-L85)

```python
class Segmentation:
    """Per-cell integer labelling of one region of the spatial grid.

    Produced by :func:`segment_domain` (connected components of a signed
    distance field) or by :func:`pymrm.construct_ibm_particles` (one label per
    particle, which keeps touching particles distinct).  The per-segment
    helpers (:func:`crossing_segments`, :func:`segment_values`,
    :func:`combine_interface_conditions`, :func:`wall_patch`,
    :func:`wall_values`, :func:`segment_field`) work with either source.

    Attributes
    ----------
    labels : ndarray of int
        Integer label field with the shape of the spatial grid.  ``0`` marks
        the *other* region; the labelled region carries ``1 .. n_segments``.
    n_segments : int
        Number of disjoint segments.
    region : {'negative', 'positive'}
        Which side of the interface was labelled (``sdf < 0`` or ``sdf >= 0``).
    connectivity : int
        Connectivity used for labelling (``1`` = faces, ``labels.ndim`` =
        including diagonals).  Reported as ``1`` for the particle path.
    sizes : ndarray of int, shape (n_segments,)
        Number of cells in each segment; ``sizes[s - 1]`` is the size of the
        segment with label ``s``.
    """

    labels: np.ndarray
    n_segments: int
    region: str
    connectivity: int
    sizes: np.ndarray
```

## Members

### `connectivity`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/segmentation.py#L84-L84)

### `labels`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/segmentation.py#L81-L81)

### `n_segments`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/segmentation.py#L82-L82)

### `region`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/segmentation.py#L83-L83)

### `sizes`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/segmentation.py#L85-L85)
