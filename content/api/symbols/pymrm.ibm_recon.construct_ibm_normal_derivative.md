# `pymrm.ibm_recon.construct_ibm_normal_derivative`

[Back to module page](../modules/pymrm.ibm_recon) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`construct_ibm_normal_derivative(ibm, sdf, x_c, *, degree = 2, length_scale = None, rings = 2, radius_factor = 1.0, length_scale_factor = 0.5, enlarge_factor = 1.5, min_points_factor = 1.5, weight_power = 4, interface_penalty = 1.0, cond_max = 100000000.0, moment_tol = 1e-08, weight_norm_max = 100.0, connectivity = 'flood', normals = None)`

## Summary

Construct one-sided normal-derivative operators for every IBM crossing.

## Documentation

### Parameters

- `ibm` (*IBM*)
  Immersed-boundary data from `pymrm.construct_ibm` (or the
  particle front end `pymrm.construct_ibm_particles`).

- `sdf` (*array_like*)
  Cell-centred field whose sign classifies the regions (``sdf < 0``
  solid).  Usually the signed-distance field used to build *ibm*; with
  the particle front end pass ``ParticleIBMInfo.pseudo_sdf``.  When
  *normals* are supplied the field is used only for region
  classification and stencil selection, not differentiated for normals.

- `x_c` (*array_like or list of array_like*)
  Cell-centre coordinates, one 1-D array per spatial axis.

- `degree` (*int or ndarray of int, optional*)
  Target polynomial degree (default 2).  A per-crossing array caps the
  degree individually (hook for solution-adaptive order control).
  ``0`` forces the two-point normal formula.

- `length_scale` (*None, float or ndarray, optional*)
  Relevant physical length scale ``L`` of the fields near the interface
  (particle size, boundary-layer thickness, ...).  Stencil radii never
  exceed ``length_scale_factor * L``; when too few points fit under the
  cap the degree is lowered instead of reaching farther.  ``None``
  (default) means the grid is assumed to resolve all relevant scales.

- `rings` (*int, optional*)
  Nominal stencil extent in cells; the geometric radius cap is
  ``radius_factor * rings * h_local``.

- `radius_factor, length_scale_factor, enlarge_factor` (*float, optional*)
  Radius-cap tuning; see above.  On rejection the radius is enlarged
  once by *enlarge_factor* (never beyond the length-scale cap) before
  the degree is lowered.

- `min_points_factor` (*float, optional*)
  Accept degree ``p`` (``M_p`` monomials) only with at least
  ``ceil(min_points_factor * (M_p - 1))`` stencil points.

- `weight_power, interface_penalty` (*float, optional*)
  Minimum-norm weights ``q_i = 1 + r_i**weight_power`` (scaled
  coordinates) and the interface-node weight.

- `cond_max, moment_tol, weight_norm_max` (*float, optional*)
  Acceptance thresholds on the moment-matrix condition number, the
  moment residual and the ``h``-scaled 1-norm of the weights.

- `connectivity` (*{'flood', 'halfspace', 'none'}, optional*)
  Same-side visibility filter.  ``'flood'`` (default, most robust)
  keeps only candidates flood-fill connected to the cut cell within the
  candidate set; ``'halfspace'`` uses a cheap normal half-space test.

- `normals` (*ndarray, shape (n_crossings, ndim_s), optional*)
  Override the SDF-gradient normals (e.g. analytic normals).

### Returns

- `IBMNormalDerivative`

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L636-L755)

```python
def construct_ibm_normal_derivative(ibm, sdf, x_c, *, degree=2,
                                    length_scale=None, rings=2,
                                    radius_factor=1.0, length_scale_factor=0.5,
                                    enlarge_factor=1.5, min_points_factor=1.5,
                                    weight_power=4, interface_penalty=1.0,
                                    cond_max=1e8, moment_tol=1e-8,
                                    weight_norm_max=100.0, connectivity="flood",
                                    normals=None):
    """Construct one-sided normal-derivative operators for every IBM crossing.

    Parameters
    ----------
    ibm : IBM
        Immersed-boundary data from :func:`pymrm.construct_ibm` (or the
        particle front end :func:`pymrm.construct_ibm_particles`).
    sdf : array_like
        Cell-centred field whose sign classifies the regions (``sdf < 0``
        solid).  Usually the signed-distance field used to build *ibm*; with
        the particle front end pass ``ParticleIBMInfo.pseudo_sdf``.  When
        *normals* are supplied the field is used only for region
        classification and stencil selection, not differentiated for normals.
    x_c : array_like or list of array_like
        Cell-centre coordinates, one 1-D array per spatial axis.
    degree : int or ndarray of int, optional
        Target polynomial degree (default 2).  A per-crossing array caps the
        degree individually (hook for solution-adaptive order control).
        ``0`` forces the two-point normal formula.
    length_scale : None, float or ndarray, optional
        Relevant physical length scale ``L`` of the fields near the interface
        (particle size, boundary-layer thickness, ...).  Stencil radii never
        exceed ``length_scale_factor * L``; when too few points fit under the
        cap the degree is lowered instead of reaching farther.  ``None``
        (default) means the grid is assumed to resolve all relevant scales.
    rings : int, optional
        Nominal stencil extent in cells; the geometric radius cap is
        ``radius_factor * rings * h_local``.
    radius_factor, length_scale_factor, enlarge_factor : float, optional
        Radius-cap tuning; see above.  On rejection the radius is enlarged
        once by *enlarge_factor* (never beyond the length-scale cap) before
        the degree is lowered.
    min_points_factor : float, optional
        Accept degree ``p`` (``M_p`` monomials) only with at least
        ``ceil(min_points_factor * (M_p - 1))`` stencil points.
    weight_power, interface_penalty : float, optional
        Minimum-norm weights ``q_i = 1 + r_i**weight_power`` (scaled
        coordinates) and the interface-node weight.
    cond_max, moment_tol, weight_norm_max : float, optional
        Acceptance thresholds on the moment-matrix condition number, the
        moment residual and the ``h``-scaled 1-norm of the weights.
    connectivity : {'flood', 'halfspace', 'none'}, optional
        Same-side visibility filter.  ``'flood'`` (default, most robust)
        keeps only candidates flood-fill connected to the cut cell within the
        candidate set; ``'halfspace'`` uses a cheap normal half-space test.
    normals : ndarray, shape (n_crossings, ndim_s), optional
        Override the SDF-gradient normals (e.g. analytic normals).

    Returns
    -------
    IBMNormalDerivative
    """
    sdf = np.asarray(sdf, dtype=float)
    if sdf.shape != ibm.spatial_shape:
        raise ValueError(
            f"sdf.shape={sdf.shape} != ibm.spatial_shape={ibm.spatial_shape}")
    ndim_s = sdf.ndim
    x_c = _normalize_x_c(x_c, ndim_s)
    npnt = ibm.n_crossings

    if normals is None:
        normals = interface_normals(ibm, sdf, x_c)
    else:
        normals = np.asarray(normals, dtype=float)
        if normals.shape != (npnt, ndim_s):
            raise ValueError(
                f"normals shape {normals.shape} != ({npnt}, {ndim_s})")
        normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    degree_arr = np.broadcast_to(
        np.asarray(degree, dtype=np.intp), (npnt,)).copy()
    if length_scale is None:
        ls = np.full(npnt, np.inf)
    else:
        ls = np.broadcast_to(
            np.asarray(length_scale, dtype=float), (npnt,)).copy()

    hax = _axis_spacings(x_c)
    h_ref = np.array([np.median(h) for h in hax])

    region_fluid = sdf.ravel() >= 0.0
    common = dict(
        degree_target=degree_arr, length_scale=ls, rings=rings,
        radius_factor=radius_factor, length_scale_factor=length_scale_factor,
        enlarge_factor=enlarge_factor, min_points_factor=min_points_factor,
        weight_power=weight_power, interface_penalty=interface_penalty,
        cond_max=cond_max, moment_tol=moment_tol,
        weight_norm_max=weight_norm_max, connectivity=connectivity,
    )
    # Outward per side: q_out along -n (out of the fluid), q_in along +n.
    out = _build_recon_side(ibm, region_fluid, ibm.row_out, -normals,
                            x_c, hax, h_ref, side_name="outside", **common)
    inn = _build_recon_side(ibm, ~region_fluid, ibm.row_in, +normals,
                            x_c, hax, h_ref, side_name="inside", **common)

    return IBMNormalDerivative(
        normals=normals,
        alpha_out=out["alpha"], alpha_in=inn["alpha"],
        D_out=out["D"], D_in=inn["D"],
        degree_out=out["degree"], degree_in=inn["degree"],
        n_stencil_out=out["n_stencil"], n_stencil_in=inn["n_stencil"],
        radius_out=out["radius"], radius_in=inn["radius"],
        cond_out=out["cond"], cond_in=inn["cond"],
        moment_residual_out=out["moment_residual"],
        moment_residual_in=inn["moment_residual"],
        weight_norm_out=out["weight_norm"], weight_norm_in=inn["weight_norm"],
        unresolved_out=out["unresolved"], unresolved_in=inn["unresolved"],
        n_crossings=npnt,
        spatial_shape=ibm.spatial_shape, shape=ibm.shape, axes=ibm.axes,
        ns_size=ibm.ns_size, n_cells=ibm.n_cells,
        n_spatial_cells=ibm.n_spatial_cells, h_ref=h_ref,
    )
```
