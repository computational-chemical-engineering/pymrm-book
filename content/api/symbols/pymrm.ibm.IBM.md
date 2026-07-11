# `pymrm.ibm.IBM`

[Back to module page](../modules/pymrm.ibm) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`IBM()`

## Summary

Consolidated IBM crossing data for both sides of an immersed interface.

## Documentation

Each entry (index ``k``) corresponds to one *wall crossing* -- a face
between a fluid cell (outside) and a solid cell (inside).  The wall
position ``coords[k]`` is shared by both sides.

Indices are **spatial** flat indices (C-order in ``spatial_shape``), not
full-field indices.  `apply_ibm` expands them to the full field using
the ``axes`` / ``shape`` information.

### Parameters indexed by crossing (length ``n_crossings``)

n_crossings : int
    Number of wall crossings.
coords : ndarray, shape (n_crossings, ndim_spatial)
    Physical coordinates of each wall crossing (spatial dimensions only).
crossing_key : ndarray of int
    Canonical face identifier.
axis : ndarray of int
    Spatial axis of each crossing.
direction : ndarray of int
    Direction (+1 or -1) from ``row_out`` to ``ghost_out``.

### Outside (fluid cut-cell) fields

row_out, ghost_out : ndarray of int
    Spatial flat indices of the fluid cut cell and its solid ghost
    neighbour.
opp_out : ndarray of int
    Spatial flat index of the opposite fluid neighbour (``-1`` when
    unavailable).
coef_c_out, coef_o_out, coef_w_out, coef_w_sib_out : ndarray of float
    Lagrange coefficients.
sib_out : ndarray of int
    Crossing index of the sandwich sibling (``-1`` if not a sandwich).
row_scale_out : ndarray of float, shape (n_spatial_cells,)
    Per-spatial-cell conditioning scale for the outside (fluid cut) rows.

### Inside (solid cut-cell) fields

row_in, ghost_in, opp_in, coef_c_in, coef_o_in, coef_w_in,
coef_w_sib_in, sib_in, row_scale_in : analogous inside fields.

### Shape information

spatial_shape : tuple
    Shape of the SDF / spatial grid.
shape : tuple
    Full field shape (spatial + non-spatial axes).
axes : tuple of int
    Which axes of ``shape`` are spatial.
ns_shape : tuple
    Non-spatial dimensions of ``shape``.
ns_size : int
    Product of non-spatial dims (1 when purely spatial).
n_cells : int
    Total number of cells, ``math.prod(shape)``.
n_spatial_cells : int
    Number of spatial cells, ``math.prod(spatial_shape)``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L113-L207)

```python
class IBM:
    """Consolidated IBM crossing data for both sides of an immersed interface.

    Each entry (index ``k``) corresponds to one *wall crossing* -- a face
    between a fluid cell (outside) and a solid cell (inside).  The wall
    position ``coords[k]`` is shared by both sides.

    Indices are **spatial** flat indices (C-order in ``spatial_shape``), not
    full-field indices.  :func:`apply_ibm` expands them to the full field using
    the ``axes`` / ``shape`` information.

    Parameters indexed by crossing (length ``n_crossings``)
    --------------------------------------------------------
    n_crossings : int
        Number of wall crossings.
    coords : ndarray, shape (n_crossings, ndim_spatial)
        Physical coordinates of each wall crossing (spatial dimensions only).
    crossing_key : ndarray of int
        Canonical face identifier.
    axis : ndarray of int
        Spatial axis of each crossing.
    direction : ndarray of int
        Direction (+1 or -1) from ``row_out`` to ``ghost_out``.

    Outside (fluid cut-cell) fields
    --------------------------------
    row_out, ghost_out : ndarray of int
        Spatial flat indices of the fluid cut cell and its solid ghost
        neighbour.
    opp_out : ndarray of int
        Spatial flat index of the opposite fluid neighbour (``-1`` when
        unavailable).
    coef_c_out, coef_o_out, coef_w_out, coef_w_sib_out : ndarray of float
        Lagrange coefficients.
    sib_out : ndarray of int
        Crossing index of the sandwich sibling (``-1`` if not a sandwich).
    row_scale_out : ndarray of float, shape (n_spatial_cells,)
        Per-spatial-cell conditioning scale for the outside (fluid cut) rows.

    Inside (solid cut-cell) fields
    --------------------------------
    row_in, ghost_in, opp_in, coef_c_in, coef_o_in, coef_w_in,
    coef_w_sib_in, sib_in, row_scale_in : analogous inside fields.

    Shape information
    -----------------
    spatial_shape : tuple
        Shape of the SDF / spatial grid.
    shape : tuple
        Full field shape (spatial + non-spatial axes).
    axes : tuple of int
        Which axes of ``shape`` are spatial.
    ns_shape : tuple
        Non-spatial dimensions of ``shape``.
    ns_size : int
        Product of non-spatial dims (1 when purely spatial).
    n_cells : int
        Total number of cells, ``math.prod(shape)``.
    n_spatial_cells : int
        Number of spatial cells, ``math.prod(spatial_shape)``.
    """

    n_crossings: int
    coords: np.ndarray
    crossing_key: np.ndarray
    axis: np.ndarray
    direction: np.ndarray

    row_out: np.ndarray
    ghost_out: np.ndarray
    opp_out: np.ndarray
    coef_c_out: np.ndarray
    coef_o_out: np.ndarray
    coef_w_out: np.ndarray
    coef_w_sib_out: np.ndarray
    sib_out: np.ndarray
    row_scale_out: np.ndarray

    row_in: np.ndarray
    ghost_in: np.ndarray
    opp_in: np.ndarray
    coef_c_in: np.ndarray
    coef_o_in: np.ndarray
    coef_w_in: np.ndarray
    coef_w_sib_in: np.ndarray
    sib_in: np.ndarray
    row_scale_in: np.ndarray

    spatial_shape: tuple
    shape: tuple
    axes: tuple
    ns_shape: tuple
    ns_size: int
    n_cells: int
    n_spatial_cells: int
```

## Members

### `axes`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L203-L203)

### `axis`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L178-L178)

### `coef_c_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L194-L194)

### `coef_c_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L184-L184)

### `coef_o_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L195-L195)

### `coef_o_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L185-L185)

### `coef_w_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L196-L196)

### `coef_w_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L186-L186)

### `coef_w_sib_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L197-L197)

### `coef_w_sib_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L187-L187)

### `coords`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L176-L176)

### `crossing_key`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L177-L177)

### `direction`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L179-L179)

### `ghost_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L192-L192)

### `ghost_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L182-L182)

### `n_cells`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L206-L206)

### `n_crossings`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L175-L175)

### `n_spatial_cells`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L207-L207)

### `ns_shape`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L204-L204)

### `ns_size`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L205-L205)

### `opp_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L193-L193)

### `opp_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L183-L183)

### `row_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L191-L191)

### `row_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L181-L181)

### `row_scale_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L199-L199)

### `row_scale_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L189-L189)

### `shape`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L202-L202)

### `sib_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L198-L198)

### `sib_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L188-L188)

### `spatial_shape`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L201-L201)
