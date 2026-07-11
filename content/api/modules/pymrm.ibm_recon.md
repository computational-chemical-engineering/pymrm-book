# `pymrm.ibm_recon`

[Back to modules overview](../api)

One-sided normal-derivative operators for the `pymrm` immersed boundary method.

This module provides *Layer 1* of the generalized immersed-interface coupling:
for every wall crossing of an `pymrm.ibm.IBM` object it constructs, on
each side separately, a linear formula for the outward normal derivative at the
interface point,

.. math::
    q_\text{side} \;=\; \left.\frac{\partial c}{\partial n_\text{side}}
    \right|_\Gamma \;\approx\;
    \alpha_\text{side}\, c_\Gamma^\text{side}
    \;+\; \sum_{j \in S_\text{side}} \gamma_j\, c_j ,

where :math:`c_\Gamma^\text{side}` is the (generally unknown) one-sided
interface value and :math:`S_\text{side}` contains nearby *same-side* cell
centres.  The weights are polynomially exact generalized finite-difference
(GFD) weights obtained from a minimum-weighted-norm problem.  These operators
are the building blocks for general interface conditions (conjugate diffusion,
partition coefficients, contact resistance, surface reactions) assembled in
`pymrm.ibm_coupling`.

## Sign conventions

* The stored unit normal is ``n = grad(sdf)/|grad(sdf)|`` and points from the
  solid (``sdf < 0``) into the fluid (``sdf >= 0``).
* Derivatives are **outward per side**, matching
  `pymrm.coupling.construct_interface_matrices`:
  ``q_out`` is taken along ``-n`` (out of the fluid domain) and ``q_in`` along
  ``+n`` (out of the solid domain).  For a healthy reconstruction both
  ``alpha_out`` and ``alpha_in`` are positive.

## Robustness / length-scale strategy

Stencil selection is governed by two caps: a geometric one
(``radius_factor * rings * h_local``) and a physical one
(``length_scale_factor * length_scale``).  When too few good points are
available inside the cap the polynomial degree is *lowered* instead of
reaching farther: ``p=2`` -> enlarge once -> ``p=1`` -> two-point normal
formula -> flagged unresolved.  Candidate cells must be flood-fill connected
to the cut cell through same-side cells, so points across a thin gap or a
neighbouring solid are never used.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`IBMNormalDerivative`](../symbols/pymrm.ibm_recon.IBMNormalDerivative) | class | One-sided normal-derivative operators and diagnostics per IBM crossing. |
| [`construct_ibm_normal_derivative`](../symbols/pymrm.ibm_recon.construct_ibm_normal_derivative) | function | Construct one-sided normal-derivative operators for every IBM crossing. |
| [`construct_ibm_normal_derivative_ops`](../symbols/pymrm.ibm_recon.construct_ibm_normal_derivative_ops) | function | Expand the reconstruction operators to the full field layout. |
| [`gfd_normal_derivative_weights`](../symbols/pymrm.ibm_recon.gfd_normal_derivative_weights) | function | GFD weights for a directional derivative at a single interface point. |
| [`interface_normals`](../symbols/pymrm.ibm_recon.interface_normals) | function | Unit interface normals (solid -> fluid) at each wall crossing. |

## `IBMNormalDerivative()`

[Open dedicated reference page](../symbols/pymrm.ibm_recon.IBMNormalDerivative)

One-sided normal-derivative operators and diagnostics per IBM crossing.

The outward normal derivative on each side of crossing ``k`` is

    ``q_side[k] = alpha_side[k] * c_gamma_side[k] + (D_side @ c_spatial)[k]``

with ``c_spatial`` the field on the spatial grid (flattened, C-order) and
the *outward per side* sign convention described in the module docstring.

### Attributes

- `normals` (*ndarray, shape (n_crossings, ndim_s)*)
  Unit normals, pointing from solid to fluid.

- `alpha_out, alpha_in` (*ndarray, shape (n_crossings,)*)
  Weight of the one-sided interface value in ``q_side``.

- `D_out, D_in` (*csr_array, shape (n_crossings, n_spatial_cells)*)
  Weights of the same-side cell values in ``q_side``.

- `degree_out, degree_in` (*ndarray of int*)
  Polynomial degree actually used: 2 or 1 (GFD), 0 (two-point normal
  formula), -1 (degenerate axis-direction two-point fallback).

- `n_stencil_out, n_stencil_in` (*ndarray of int*)
  Number of cell points in the stencil.

- `radius_out, radius_in` (*ndarray*)
  Physical search radius of the accepted stencil.

- `cond_out, cond_in` (*ndarray*)
  Conditioning of the GFD moment matrix (1 for two-point formulas).

- `moment_residual_out, moment_residual_in` (*ndarray*)
  Max-norm residual of the polynomial moment conditions.

- `weight_norm_out, weight_norm_in` (*ndarray*)
  ``h``-scaled 1-norm of the weights, O(1) for a healthy formula.

- `unresolved_out, unresolved_in` (*ndarray of bool*)
  True where only the degenerate axis-direction fallback was possible.

### Shape information

n_crossings : int
    Number of wall crossings (matches ``ibm.n_crossings``).
spatial_shape : tuple
    Spatial grid shape.
shape : tuple
    Full field shape (spatial + non-spatial axes).
axes : tuple of int
    Which axes of ``shape`` are spatial.
ns_size : int
    Product of the non-spatial dimensions (1 when purely spatial).
n_cells : int
    Total number of cells, ``prod(shape)``.
n_spatial_cells : int
    Number of spatial cells, ``prod(spatial_shape)``.
h_ref : ndarray, shape (ndim_spatial,)
    Median cell-centre spacing along each spatial axis (reference scale
    for the GFD weights).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L70-L154)

## Members

### `D_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L130-L130)

### `D_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L129-L129)

### `alpha_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L128-L128)

### `alpha_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L127-L127)

### `axes`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L150-L150)

### `cond_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L139-L139)

### `cond_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L138-L138)

### `degree_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L133-L133)

### `degree_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L132-L132)

### `h_ref`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L154-L154)

### `moment_residual_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L141-L141)

### `moment_residual_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L140-L140)

### `n_cells`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L152-L152)

### `n_crossings`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L147-L147)

### `n_spatial_cells`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L153-L153)

### `n_stencil_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L135-L135)

### `n_stencil_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L134-L134)

### `normals`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L125-L125)

### `ns_size`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L151-L151)

### `radius_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L137-L137)

### `radius_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L136-L136)

### `shape`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L149-L149)

### `spatial_shape`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L148-L148)

### `unresolved_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L145-L145)

### `unresolved_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L144-L144)

### `weight_norm_in`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L143-L143)

### `weight_norm_out`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L142-L142)

## `construct_ibm_normal_derivative(ibm, sdf, x_c, *, degree = 2, length_scale = None, rings = 2, radius_factor = 1.0, length_scale_factor = 0.5, enlarge_factor = 1.5, min_points_factor = 1.5, weight_power = 4, interface_penalty = 1.0, cond_max = 100000000.0, moment_tol = 1e-08, weight_norm_max = 100.0, connectivity = 'flood', normals = None)`

[Open dedicated reference page](../symbols/pymrm.ibm_recon.construct_ibm_normal_derivative)

Construct one-sided normal-derivative operators for every IBM crossing.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L636-L755)

## `construct_ibm_normal_derivative_ops(ibm, recon)`

[Open dedicated reference page](../symbols/pymrm.ibm_recon.construct_ibm_normal_derivative_ops)

Expand the reconstruction operators to the full field layout.

Returns operators acting on the *flattened full field* ``c`` (including
non-spatial axes) with rows ordered ``k * ns_size + j`` for crossing ``k``
and non-spatial layer ``j`` — the same column ordering used by the
``G_out``/``G_in`` source matrices of `pymrm.apply_ibm`:

    ``q_side.ravel() = alpha_side_full * w_side + N_side @ c.ravel()``

### Parameters

- `ibm` (*IBM*)

- `recon` (*IBMNormalDerivative*)

### Returns

- `alpha_out_full` (*ndarray, shape (n_crossings * ns_size,)*)

- `N_out` (*csr_array, shape (n_crossings * ns_size, n_cells)*)

- `alpha_in_full` (*ndarray, shape (n_crossings * ns_size,)*)

- `N_in` (*csr_array, shape (n_crossings * ns_size, n_cells)*)

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L762-L804)

## `gfd_normal_derivative_weights(x_gamma, x_cells, direction, degree = 2, hvec = None, weight_power = 4, interface_penalty = 1.0)`

[Open dedicated reference page](../symbols/pymrm.ibm_recon.gfd_normal_derivative_weights)

GFD weights for a directional derivative at a single interface point.

Returns ``alpha``, ``gamma`` and diagnostics such that

    ``dc/du|_Gamma ~= alpha * c_gamma + gamma @ c_cells``

is exact for all polynomials up to *degree*.  This is the single-point
convenience form of the batched kernel used by
`construct_ibm_normal_derivative`; *direction* is the (not necessarily
unit) derivative direction ``u``.

### Parameters

- `x_gamma` (*array_like, shape (ndim,)*)
  Interface point.

- `x_cells` (*array_like, shape (N, ndim)*)
  Same-side cell centres.

- `direction` (*array_like, shape (ndim,)*)
  Derivative direction; normalized internally.

- `degree` (*int, optional*)
  Polynomial exactness degree (default 2).

- `hvec` (*array_like, shape (ndim,), optional*)
  Per-axis coordinate scaling.  Defaults to the median point distance.

- `weight_power` (*float, optional*)
  Distance-penalty exponent: ``q_i = 1 + r_i**weight_power`` in scaled
  coordinates (default 4).

- `interface_penalty` (*float, optional*)
  Minimum-norm weight of the interface node (default 1.0).

### Returns

- `alpha` (*float*)
  Weight of the interface value.

- `gamma` (*ndarray, shape (N,)*)
  Weights of the cell values.

- `info` (*dict*)
  ``cond`` and ``moment_residual`` diagnostics.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L244-L307)

## `interface_normals(ibm, sdf, x_c)`

[Open dedicated reference page](../symbols/pymrm.ibm_recon.interface_normals)

Unit interface normals (solid -> fluid) at each wall crossing.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L340-L391)
