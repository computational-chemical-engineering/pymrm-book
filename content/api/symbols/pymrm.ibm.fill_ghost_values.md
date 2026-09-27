# `pymrm.ibm.fill_ghost_values`

[Back to module page](../modules/pymrm.ibm) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`fill_ghost_values(ibm, x_c, field, wall_values = 0.0, side = 'out', theta_min = 0.25)`

## Summary

Copy of ``field`` with interface-adjacent ghost cells filled.

## Documentation

Ghost cells shared by several crossings receive the average of the
per-crossing reconstructions of `reconstruct_ghost_values`; all
other cells keep their original values.  The result is suitable for
interpolating cell-centered state variables to faces near the immersed
boundary (e.g. with `pymrm.interp_cntr_to_stagg`).

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/ibm.py#L1204-L1228)

```python
def fill_ghost_values(ibm, x_c, field, wall_values=0.0, side="out",
                      theta_min=0.25):
    """Copy of ``field`` with interface-adjacent ghost cells filled.

    Ghost cells shared by several crossings receive the average of the
    per-crossing reconstructions of :func:`reconstruct_ghost_values`; all
    other cells keep their original values.  The result is suitable for
    interpolating cell-centered state variables to faces near the immersed
    boundary (e.g. with :func:`pymrm.interp_cntr_to_stagg`).
    """
    ghosts, vals = reconstruct_ghost_values(
        ibm, x_c, field, wall_values=wall_values, side=side,
        theta_min=theta_min)
    field = np.asarray(field, dtype=float)
    nd = len(ibm.spatial_shape)
    trailing = field.shape[nd:]
    out = field.reshape(ibm.n_spatial_cells, -1).copy()
    vals2 = vals.reshape(vals.shape[0], -1)
    sums = np.zeros_like(out)
    counts = np.zeros(out.shape[0])
    np.add.at(sums, ghosts, vals2)
    np.add.at(counts, ghosts, 1.0)
    filled = counts > 0
    out[filled] = sums[filled] / counts[filled, None]
    return out.reshape(field.shape)
```
