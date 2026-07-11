# `pymrm.ibm_recon.interface_normals`

[Back to module page](../modules/pymrm.ibm_recon) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`interface_normals(ibm, sdf, x_c)`

## Summary

Unit interface normals (solid -> fluid) at each wall crossing.

## Documentation

The cell-centred gradient of *sdf* is computed with `numpy.gradient`
(non-equidistant aware) and averaged over the two cut cells of each
crossing.  Crossings with a degenerate gradient (kinks of the level set,
e.g. near medial axes of thin solids) fall back to the axis-aligned
normal of the crossing.

### Parameters

- `ibm` (*IBM*)
  Immersed-boundary data from `pymrm.construct_ibm`.

- `sdf` (*array_like*)
  Signed-distance (or level-set) field at the spatial cell centres.

- `x_c` (*array_like or list of array_like*)
  Cell-centre coordinates, one 1-D array per spatial axis.

### Returns

- `ndarray, shape (n_crossings, ndim_spatial)`

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L340-L391)

```python
def interface_normals(ibm, sdf, x_c):
    """Unit interface normals (solid -> fluid) at each wall crossing.

    The cell-centred gradient of *sdf* is computed with :func:`numpy.gradient`
    (non-equidistant aware) and averaged over the two cut cells of each
    crossing.  Crossings with a degenerate gradient (kinks of the level set,
    e.g. near medial axes of thin solids) fall back to the axis-aligned
    normal of the crossing.

    Parameters
    ----------
    ibm : IBM
        Immersed-boundary data from :func:`pymrm.construct_ibm`.
    sdf : array_like
        Signed-distance (or level-set) field at the spatial cell centres.
    x_c : array_like or list of array_like
        Cell-centre coordinates, one 1-D array per spatial axis.

    Returns
    -------
    ndarray, shape (n_crossings, ndim_spatial)
    """
    sdf = np.asarray(sdf, dtype=float)
    ndim_s = sdf.ndim
    x_c = _normalize_x_c(x_c, ndim_s)

    if ibm.n_crossings == 0:
        return np.empty((0, ndim_s))

    if ndim_s == 1:
        grads = [np.gradient(sdf, x_c[0])]
    else:
        grads = np.gradient(sdf, *x_c)
    g = np.stack([gr.ravel() for gr in grads], axis=1)   # (n_spatial, ndim_s)

    # Interpolate the two cut-cell gradients to the wall position:
    # x_w = x_out + theta * (x_in - x_out) with theta from the sdf values.
    sdf_flat = sdf.ravel()
    sdf_o = sdf_flat[ibm.row_out]
    sdf_i = sdf_flat[ibm.row_in]
    denom = sdf_o - sdf_i
    theta = np.where(denom != 0.0, sdf_o / np.where(denom == 0.0, 1.0, denom),
                     0.5)
    theta = np.clip(theta, 0.0, 1.0)[:, np.newaxis]
    n = (1.0 - theta) * g[ibm.row_out] + theta * g[ibm.row_in]
    norm = np.linalg.norm(n, axis=1)
    med = np.median(norm)
    degen = norm <= max(1e-6 * med, 1e-300)
    if np.any(degen):
        n[degen] = _axis_fallback_normals(ibm, degen)
        norm = np.linalg.norm(n, axis=1)
    return n / norm[:, np.newaxis]
```
