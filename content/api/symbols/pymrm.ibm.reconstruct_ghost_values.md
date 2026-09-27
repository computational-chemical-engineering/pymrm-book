# `pymrm.ibm.reconstruct_ghost_values`

[Back to module page](../modules/pymrm.ibm) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`reconstruct_ghost_values(ibm, x_c, field, wall_values = 0.0, side = 'out', theta_min = 0.25)`

## Summary

Reconstruct per-crossing ghost-cell values of a cell-centered field.

## Documentation

For every wall crossing the value of ``field`` at the *ghost* cell center
(the first cell on the other side of the immersed interface) is
extrapolated along the crossing axis from the same-side cells and the
Dirichlet wall value.  This is useful for evaluating state-dependent
coefficients (e.g. composition-dependent diffusivities) at faces near the
immersed boundary, where neighbouring cell values are missing.

The ghost value of a field is direction dependent (one solid cell can be
the ghost of several crossings, with slightly different reconstructions);
values are therefore returned per crossing.  Use
`fill_ghost_values` for a filled (averaged) copy of the field.

Reconstruction: second-order Lagrange through the cut cell, its opposite
same-side neighbour, and the wall point, evaluated at the ghost center.
When the wall lies within ``theta_min`` of the cut-cell center (measured
as a fraction of the center-to-ghost distance), the cut-cell value is
skipped and a first-order (linear) reconstruction through the opposite
neighbour and the wall point is used instead: the second-order formula is
an unstable extrapolation when two of its nodes nearly coincide.  Without
an opposite neighbour the reconstruction is linear through the cut cell
and the wall, or the wall value itself when additionally
``theta < theta_min``.

### Parameters

- `ibm` (*IBM*)
  Immersed-boundary data from `construct_ibm`.

- `x_c` (*array_like or list of array_like*)
  Cell-center coordinates per spatial axis (same as ``construct_ibm``).

- `field` (*array_like*)
  Cell-centered field.  Shape must start with ``ibm.spatial_shape``;
  trailing (non-spatial) dimensions are allowed and handled
  elementwise.

- `wall_values` (*array_like, optional*)
  Dirichlet wall values; broadcastable to
  ``(n_crossings, *trailing_shape)``.

- `side` (*{'out', 'in'}, optional*)
  Reconstruct from the fluid side (``'out'``, default) or solid side.

- `theta_min` (*float, optional*)
  Threshold on the wall position fraction below which the
  reconstruction switches from second to first order.

### Returns

- `ghost_index` (*ndarray of int, shape (n_crossings,)*)
  Spatial flat index of each ghost cell.

- `ghost_values` (*ndarray, shape (n_crossings, *trailing_shape)*)
  Reconstructed field values at the ghost-cell centers.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/ibm.py#L1085-L1201)

```python
def reconstruct_ghost_values(ibm, x_c, field, wall_values=0.0, side="out",
                             theta_min=0.25):
    """Reconstruct per-crossing ghost-cell values of a cell-centered field.

    For every wall crossing the value of ``field`` at the *ghost* cell center
    (the first cell on the other side of the immersed interface) is
    extrapolated along the crossing axis from the same-side cells and the
    Dirichlet wall value.  This is useful for evaluating state-dependent
    coefficients (e.g. composition-dependent diffusivities) at faces near the
    immersed boundary, where neighbouring cell values are missing.

    The ghost value of a field is direction dependent (one solid cell can be
    the ghost of several crossings, with slightly different reconstructions);
    values are therefore returned per crossing.  Use
    :func:`fill_ghost_values` for a filled (averaged) copy of the field.

    Reconstruction: second-order Lagrange through the cut cell, its opposite
    same-side neighbour, and the wall point, evaluated at the ghost center.
    When the wall lies within ``theta_min`` of the cut-cell center (measured
    as a fraction of the center-to-ghost distance), the cut-cell value is
    skipped and a first-order (linear) reconstruction through the opposite
    neighbour and the wall point is used instead: the second-order formula is
    an unstable extrapolation when two of its nodes nearly coincide.  Without
    an opposite neighbour the reconstruction is linear through the cut cell
    and the wall, or the wall value itself when additionally
    ``theta < theta_min``.

    Parameters
    ----------
    ibm : IBM
        Immersed-boundary data from :func:`construct_ibm`.
    x_c : array_like or list of array_like
        Cell-center coordinates per spatial axis (same as ``construct_ibm``).
    field : array_like
        Cell-centered field.  Shape must start with ``ibm.spatial_shape``;
        trailing (non-spatial) dimensions are allowed and handled
        elementwise.
    wall_values : array_like, optional
        Dirichlet wall values; broadcastable to
        ``(n_crossings, *trailing_shape)``.
    side : {'out', 'in'}, optional
        Reconstruct from the fluid side (``'out'``, default) or solid side.
    theta_min : float, optional
        Threshold on the wall position fraction below which the
        reconstruction switches from second to first order.

    Returns
    -------
    ghost_index : ndarray of int, shape (n_crossings,)
        Spatial flat index of each ghost cell.
    ghost_values : ndarray, shape (n_crossings, *trailing_shape)
        Reconstructed field values at the ghost-cell centers.
    """
    nd = len(ibm.spatial_shape)
    if isinstance(x_c, np.ndarray) and x_c.ndim == 1 and nd == 1:
        x_c = [np.asarray(x_c, dtype=float)]
    else:
        x_c = [np.asarray(xc, dtype=float) for xc in x_c]

    rows = getattr(ibm, f"row_{side}")
    ghosts = getattr(ibm, f"ghost_{side}")
    opps = getattr(ibm, f"opp_{side}")
    npnt = ibm.n_crossings

    field = np.asarray(field, dtype=float)
    trailing = field.shape[nd:]
    f_flat = field.reshape(ibm.n_spatial_cells, -1)
    w = np.broadcast_to(
        np.asarray(wall_values, dtype=float),
        (npnt, *trailing)).reshape(npnt, -1)

    def _coord_along_axis(flat_idx):
        idx = np.unravel_index(np.maximum(flat_idx, 0), ibm.spatial_shape)
        per_axis = np.stack([x_c[a][idx[a]] for a in range(nd)], axis=0)
        return per_axis[ibm.axis, np.arange(npnt)]

    x_row = _coord_along_axis(rows)
    x_ghost = _coord_along_axis(ghosts)
    x_opp = _coord_along_axis(opps)
    x_w = ibm.coords[np.arange(npnt), ibm.axis]

    theta = (x_w - x_row) / (x_ghost - x_row)
    has_opp = opps >= 0
    use_first = theta < theta_min

    L_row = np.zeros(npnt)
    L_opp = np.zeros(npnt)
    L_w = np.zeros(npnt)

    # second order: Lagrange through (x_opp, x_row, x_w) at x_ghost
    m = has_opp & ~use_first
    if m.any():
        xo, xr, xw, xg = x_opp[m], x_row[m], x_w[m], x_ghost[m]
        L_opp[m] = (xg - xr) * (xg - xw) / ((xo - xr) * (xo - xw))
        L_row[m] = (xg - xo) * (xg - xw) / ((xr - xo) * (xr - xw))
        L_w[m] = (xg - xo) * (xg - xr) / ((xw - xo) * (xw - xr))
    # first order through (x_opp, x_w): skip the too-close cut cell
    m = has_opp & use_first
    if m.any():
        xo, xw, xg = x_opp[m], x_w[m], x_ghost[m]
        L_opp[m] = (xg - xw) / (xo - xw)
        L_w[m] = (xg - xo) / (xw - xo)
    # no opposite neighbour: linear through (x_row, x_w) ...
    m = ~has_opp & ~use_first
    if m.any():
        xr, xw, xg = x_row[m], x_w[m], x_ghost[m]
        L_row[m] = (xg - xw) / (xr - xw)
        L_w[m] = (xg - xr) / (xw - xr)
    # ... or the wall value itself when the cut cell is also too close
    m = ~has_opp & use_first
    L_w[m] = 1.0

    f_row = f_flat[rows]
    f_opp = f_flat[np.maximum(opps, 0)]
    vals = (L_row[:, None] * f_row + L_opp[:, None] * f_opp
            + L_w[:, None] * w)
    return ghosts.copy(), vals.reshape(npnt, *trailing)
```
