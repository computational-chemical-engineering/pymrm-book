# `pymrm.particles.construct_ibm_particles`

[Back to module page](../modules/pymrm.particles) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`construct_ibm_particles(particles, x_c, *, axes = None, shape = None, rescale = True, contact = 'no_flux', halo = 2, fill_value = None)`

## Summary

Build immersed-boundary data directly from a particle assembly.

## Documentation

### Parameters

- `particles` (*sequence of Particle*)

- `x_c` (*array_like or list of array_like*)
  Cell-centre coordinates, one 1-D array per spatial axis.

- `axes, shape, rescale` (*see `pymrm.construct_ibm`.*)

- `contact` (*{'no_flux', 'merge', 'error'}, optional*)
  Policy for solid–solid faces between two different particles whose
  surfaces are separated by a sub-cell gap (see the module docstring).
  Genuinely overlapping particles are always merged.

- `halo` (*int, optional*)
  Extra cells around each particle's bounding box when classifying.

- `fill_value` (*float, optional*)
  ``pseudo_sdf`` value for cells not covered by any particle window
  (default: 4× the largest cell spacing — any positive value works,
  only the sign is used downstream).

### Returns

- `ibm` (*IBM*)
  Standard immersed-boundary container; all of `pymrm.apply_ibm`,
  `pymrm.apply_ibm_interface`, etc. apply unchanged.

- `info` (*ParticleIBMInfo*)
  Ownership, exact normals, contact bookkeeping, ``pseudo_sdf`` and a
  per-particle `~pymrm.segmentation.Segmentation`.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/particles.py#L520-L712)

```python
def construct_ibm_particles(particles, x_c, *, axes=None, shape=None,
                            rescale=True, contact="no_flux", halo=2,
                            fill_value=None):
    """Build immersed-boundary data directly from a particle assembly.

    Parameters
    ----------
    particles : sequence of Particle
    x_c : array_like or list of array_like
        Cell-centre coordinates, one 1-D array per spatial axis.
    axes, shape, rescale : see :func:`pymrm.construct_ibm`.
    contact : {'no_flux', 'merge', 'error'}, optional
        Policy for solid–solid faces between two different particles whose
        surfaces are separated by a sub-cell gap (see the module docstring).
        Genuinely overlapping particles are always merged.
    halo : int, optional
        Extra cells around each particle's bounding box when classifying.
    fill_value : float, optional
        ``pseudo_sdf`` value for cells not covered by any particle window
        (default: 4× the largest cell spacing — any positive value works,
        only the sign is used downstream).

    Returns
    -------
    ibm : IBM
        Standard immersed-boundary container; all of :func:`pymrm.apply_ibm`,
        :func:`pymrm.apply_ibm_interface`, etc. apply unchanged.
    info : ParticleIBMInfo
        Ownership, exact normals, contact bookkeeping, ``pseudo_sdf`` and a
        per-particle :class:`~pymrm.segmentation.Segmentation`.
    """
    x_c = _normalize_x_c(x_c)
    spatial_shape = tuple(x.size for x in x_c)
    ndim = len(spatial_shape)
    n_spatial = math.prod(spatial_shape)
    strides = np.array([math.prod(spatial_shape[a + 1:]) for a in range(ndim)],
                       dtype=np.intp)
    if contact not in ("no_flux", "merge", "error"):
        raise ValueError(
            f"contact must be 'no_flux', 'merge' or 'error', got {contact!r}")
    for p in particles:
        if p.ndim != ndim:
            raise ValueError(
                f"particle dimension {p.ndim} != grid dimension {ndim}")
    if fill_value is None:
        fill_value = 4.0 * max(float(np.max(np.diff(x))) if x.size > 1 else 1.0
                               for x in x_c)

    # --- classification: owner (deepest level) + pseudo union level --------
    owner = np.full(n_spatial, -1, dtype=np.intp)
    depth = np.full(n_spatial, np.inf)
    pseudo = np.full(n_spatial, float(fill_value))
    for i, p in enumerate(particles):
        sl = _window(p, x_c, halo)
        if sl is None:
            continue
        widx = _window_flat(sl, spatial_shape, strides).ravel()
        lv = np.asarray(p.level(_window_coords(sl, x_c)), dtype=float).ravel()
        np.minimum.at(pseudo, widx, lv)
        better = lv < np.minimum(depth[widx], 0.0)
        bidx = widx[better]
        owner[bidx] = i
        depth[bidx] = lv[better]
    solid_flat = owner >= 0
    pseudo = np.where(solid_flat, depth, pseudo)

    # --- face scan ----------------------------------------------------------
    solid_grid = solid_flat.reshape(spatial_shape)
    owner_grid = owner.reshape(spatial_shape)

    keys, thetas = [], []                       # directed theta registry
    contact_cols = {k: [] for k in ("lo", "hi", "i", "j", "s_i", "s_j")}
    for a in range(ndim):
        nb_solid, valid = _neighbor(solid_grid, a, +1)
        nb_owner, _ = _neighbor(owner_grid, a, +1)
        lo = np.flatnonzero((valid & (solid_grid != nb_solid)).ravel())
        if lo.size:
            hi = lo + strides[a]
            # fluid–solid crossing faces: owner of the solid cell intersects
            lo_solid = solid_flat[lo]
            own = np.where(lo_solid, owner[lo], owner[hi])
            p_lo = _cell_coords(lo, x_c, spatial_shape)
            p_hi = _cell_coords(hi, x_c, spatial_shape)
            s = np.empty(lo.size)
            for i in np.unique(own):
                m = own == i
                s[m] = particles[i].intersect(p_lo[m], p_hi[m])
            keys.append(_FaceThetaMap.pack(lo, a, +1, ndim))
            thetas.append(s)
            keys.append(_FaceThetaMap.pack(hi, a, -1, ndim))
            thetas.append(1.0 - s)
        # solid–solid faces between different particles
        cc = np.flatnonzero((valid & solid_grid & nb_solid
                             & (owner_grid != nb_owner)).ravel())
        if cc.size:
            hi = cc + strides[a]
            i_arr, j_arr = owner[cc], owner[hi]
            p_lo = _cell_coords(cc, x_c, spatial_shape)
            p_hi = _cell_coords(hi, x_c, spatial_shape)
            # gap test: cell strictly outside the *other* particle
            out_j = np.empty(cc.size, dtype=bool)   # level_j(p_lo) > 0
            out_i = np.empty(cc.size, dtype=bool)   # level_i(p_hi) > 0
            s_i = np.full(cc.size, np.nan)
            s_j = np.full(cc.size, np.nan)
            for i in np.unique(np.concatenate([i_arr, j_arr])):
                m = j_arr == i
                if m.any():
                    out_j[m] = particles[i].level(p_lo[m]) > 0.0
                m = i_arr == i
                if m.any():
                    out_i[m] = particles[i].level(p_hi[m]) > 0.0
            gap = out_i & out_j
            if gap.any():
                for i in np.unique(i_arr[gap]):
                    m = gap & (i_arr == i)
                    s_i[m] = particles[i].intersect(p_lo[m], p_hi[m])
                for j in np.unique(j_arr[gap]):
                    m = gap & (j_arr == j)
                    s_j[m] = particles[j].intersect(p_lo[m], p_hi[m])
                gap &= s_i < s_j            # disjoint surface intervals
            if gap.any():
                if contact == "error":
                    raise RuntimeError(
                        f"particle IBM: {int(gap.sum())} contact face(s) "
                        "between different particles (contact='error')")
                if contact == "no_flux":
                    contact_cols["lo"].append(cc[gap])
                    contact_cols["hi"].append(hi[gap])
                    contact_cols["i"].append(i_arr[gap])
                    contact_cols["j"].append(j_arr[gap])
                    contact_cols["s_i"].append(s_i[gap])
                    contact_cols["s_j"].append(s_j[gap])
                # 'merge': nothing to do

    if keys:
        theta_map = _FaceThetaMap(np.concatenate(keys), np.concatenate(thetas),
                                  ndim)
    else:
        theta_map = _FaceThetaMap(np.empty(0, dtype=np.intp), np.empty(0), ndim)

    # --- fluid–solid crossings through the shared IBM core ------------------
    out_s, in_s, meta = _construct_ibm_core(
        solid_grid, theta_map, x_c, axes, shape, rescale, pair=False)

    # --- contact crossings (no_flux policy) ---------------------------------
    n_contact = 0
    if contact_cols["lo"]:
        lo = np.concatenate(contact_cols["lo"])
        hi = np.concatenate(contact_cols["hi"])
        part_i = np.concatenate(contact_cols["i"])
        part_j = np.concatenate(contact_cols["j"])
        s_i = np.concatenate(contact_cols["s_i"])
        s_j = np.concatenate(contact_cols["s_j"])
        n_contact = lo.size
        ax_of = np.empty(lo.size, dtype=np.intp)
        for a in range(ndim):
            ax_of[(hi - lo) == strides[a]] = a
        out_s = _append_contact_side(out_s, lo, hi, ax_of, +1, s_i,
                                     0.5 * (s_i + s_j), owner, x_c,
                                     spatial_shape, strides, ndim, rescale)
        in_s = _append_contact_side(in_s, hi, lo, ax_of, -1, 1.0 - s_j,
                                    0.5 * (s_i + s_j), owner, x_c,
                                    spatial_shape, strides, ndim, rescale)

    ibm = _pair_sides_to_ibm(out_s, in_s, **meta)

    # --- normals + per-crossing bookkeeping ---------------------------------
    crossing_particle = owner[ibm.row_in]
    # A regular crossing has a fluid out cell; a contact crossing's out cell
    # is solid (it belongs to the partner particle).
    contact_mask = solid_flat[ibm.row_out]
    contact_partner = np.where(contact_mask, owner[ibm.row_out], -1)

    # The in-side particle's outward normal serves both crossing types: it
    # points solid -> fluid on regular crossings, and towards the partner
    # (the out side) on contact crossings.
    normals = np.empty((ibm.n_crossings, ndim))
    for i in np.unique(crossing_particle):
        m = crossing_particle == i
        normals[m] = particles[i].normal(ibm.coords[m])

    labels = np.where(solid_flat, owner + 1, 0).reshape(spatial_shape)
    sizes = np.bincount(labels.ravel(),
                        minlength=len(particles) + 1)[1:].astype(np.intp)
    seg = Segmentation(labels=labels, n_segments=len(particles),
                       region="negative", connectivity=1, sizes=sizes)

    info = ParticleIBMInfo(
        owner=owner_grid, crossing_particle=crossing_particle,
        contact=contact_mask, contact_partner=contact_partner,
        normals=normals, pseudo_sdf=pseudo.reshape(spatial_shape),
        segmentation=seg)
    return ibm, info
```
