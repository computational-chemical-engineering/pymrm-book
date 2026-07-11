# `pymrm.segmentation`

[Back to modules overview](../api)

SDF-based domain segmentation for immersed boundaries in `pymrm`.

Immersed boundary conditions are specified per *wall crossing* rather than on a
grid-aligned face, so the spatial broadcasting that domain-wall boundary
conditions enjoy (a single value copied along a wall) is not directly
available.  In practice the most useful spatial pattern is *piecewise constant
per body*: give every dispersed element (a disjoint region of the signed
distance field) its own interface condition.  This module restores that
workflow.

`segment_domain` labels the disjoint regions of the SDF with
`scipy.ndimage.label`.  `crossing_segments` maps each IBM crossing
to the label of the body it bounds, and `segment_values` /
`combine_interface_conditions` expand per-segment data to the
per-crossing arrays consumed by `pymrm.apply_ibm` and
`pymrm.apply_ibm_interface`.  Where a body touches the domain boundary,
`wall_patch` / `wall_values` produce broadcast-ready coefficients
for the ordinary ``{a, b, d}`` wall boundary conditions, so a wall-touching
body can carry the same condition on its wall patch as on its immersed part.
`wall_contact` reports which bodies reach a domain wall — useful on the
fluid side (``region="positive"``) to detect isolated no-flux pockets that
would otherwise make the operator singular.

The ``region`` argument selects which side of the interface is segmented:
``"negative"`` (the default, ``sdf < 0`` solid bodies) or ``"positive"``
(``sdf >= 0`` fluid regions), matching the solid/fluid convention of
`pymrm.construct_ibm`.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`Segmentation`](../symbols/pymrm.segmentation.Segmentation) | class | Per-cell integer labelling of one region of the spatial grid. |
| [`combine_interface_conditions`](../symbols/pymrm.segmentation.combine_interface_conditions) | function | Merge per-segment interface conditions into one per-crossing ``ic``. |
| [`crossing_segments`](../symbols/pymrm.segmentation.crossing_segments) | function | Segment label of the body bounded by each IBM crossing. |
| [`segment_domain`](../symbols/pymrm.segmentation.segment_domain) | function | Label the disjoint regions of a signed distance field. |
| [`segment_field`](../symbols/pymrm.segmentation.segment_field) | function | Expand per-segment values to a per-cell spatial field. |
| [`segment_values`](../symbols/pymrm.segmentation.segment_values) | function | Expand per-segment values to a per-crossing array for `pymrm.apply_ibm`. |
| [`wall_contact`](../symbols/pymrm.segmentation.wall_contact) | function | Whether each segment reaches each domain wall. |
| [`wall_patch`](../symbols/pymrm.segmentation.wall_patch) | function | Segment labels on one domain wall, shaped as a full-field coefficient. |
| [`wall_values`](../symbols/pymrm.segmentation.wall_values) | function | Per-segment values on one domain wall as a full-field BC coefficient. |

## `Segmentation()`

[Open dedicated reference page](../symbols/pymrm.segmentation.Segmentation)

Per-cell integer labelling of one region of the spatial grid.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L54-L85)

## Members

### `connectivity`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L84-L84)

### `labels`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L81-L81)

### `n_segments`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L82-L82)

### `region`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L83-L83)

### `sizes`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L85-L85)

## `combine_interface_conditions(ic_by_segment, seg, ibm, *, default = None)`

[Open dedicated reference page](../symbols/pymrm.segmentation.combine_interface_conditions)

Merge per-segment interface conditions into one per-crossing ``ic``.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L435-L482)

## `crossing_segments(seg, ibm)`

[Open dedicated reference page](../symbols/pymrm.segmentation.crossing_segments)

Segment label of the body bounded by each IBM crossing.

For ``region="negative"`` the label of the *inside* (solid) cut cell is
returned; for ``region="positive"`` the *outside* (fluid) cut cell.  In
either case the cut cell lies in the segmented region, so every returned
label is in ``1 .. n_segments``.

### Parameters

- `seg` (*Segmentation*)

- `ibm` (*IBM*)

### Returns

- `ndarray of int, shape (n_crossings,)`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L142-L169)

## `segment_domain(sdf, *, region = 'negative', connectivity = 1)`

[Open dedicated reference page](../symbols/pymrm.segmentation.segment_domain)

Label the disjoint regions of a signed distance field.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L88-L128)

## `segment_field(values, seg, *, default = 0.0)`

[Open dedicated reference page](../symbols/pymrm.segmentation.segment_field)

Expand per-segment values to a per-cell spatial field.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L287-L308)

## `segment_values(values, seg, ibm, *, default = None)`

[Open dedicated reference page](../symbols/pymrm.segmentation.segment_values)

Expand per-segment values to a per-crossing array for `pymrm.apply_ibm`.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L259-L284)

## `wall_contact(seg)`

[Open dedicated reference page](../symbols/pymrm.segmentation.wall_contact)

Whether each segment reaches each domain wall.

### Returns

- `ndarray of bool, shape (n_segments, ndim_spatial, 2)`
  ``out[s - 1, a, 0]`` / ``out[s - 1, a, 1]`` is ``True`` when segment
  ``s`` has cells in the first / last layer along spatial axis ``a``.

### Notes

A fluid-side segmentation (``region="positive"``) whose segment touches no
wall is an isolated pocket; with all-Neumann surroundings it makes the
operator singular.  Detect them with
``np.flatnonzero(~wall_contact(seg).any(axis=(1, 2))) + 1``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L315-L339)

## `wall_patch(seg, ibm, axis, side)`

[Open dedicated reference page](../symbols/pymrm.segmentation.wall_patch)

Segment labels on one domain wall, shaped as a full-field coefficient.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L352-L379)

## `wall_values(values, seg, ibm, axis, side, *, default = 0.0)`

[Open dedicated reference page](../symbols/pymrm.segmentation.wall_values)

Per-segment values on one domain wall as a full-field BC coefficient.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/segmentation.py#L382-L419)
