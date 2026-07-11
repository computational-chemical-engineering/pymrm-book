# `pymrm.ibm`

[Back to modules overview](../api)

Directional ghost-cell immersed boundary method (IBM) for `pymrm`.

This module adds a *point-value*, Dirichlet directional ghost-cell immersed
boundary method for the non-equidistant finite-volume grids used throughout
`pymrm`.

## Overview

A signed-distance field (SDF) sampled at the **spatial** cell centres flags
every cell as solid (``sdf < 0``) or fluid (``sdf >= 0``).  Wherever an
axis-neighbour switches region a *wall crossing* is created.  Each crossing is
shared by exactly two rows of the operator matrix: the fluid (*outside*) cut
cell and the solid (*inside*) cut cell.  Both sides share the same geometric
wall position, so the IBM data is stored in a single `IBM` object
indexed by crossing.

For each crossing the ghost value in the fluid row is reconstructed by a
second-order Lagrange interpolation through
``{opposite fluid neighbour, fluid cell centre, wall value}`` (and
symmetrically for the solid row).  This is the same Lagrange construction
used by `pymrm.operators.construct_grad_bc` for domain boundary
conditions.

The classification and wall positions may equally be supplied by an assembly
of analytic shapes rather than a sampled field: `pymrm.construct_ibm_particles`
produces the very same `IBM` object (with exact per-particle wall
positions and normals) and everything downstream — `apply_ibm`,
`pymrm.ibm_recon`, `pymrm.ibm_coupling` — is unchanged.

## Multi-dimensional fields

The field on which the IBM operator acts may have *non-spatial* axes
(components, phases, species, etc.) in addition to the spatial axes specified
by the ``axes`` argument to `construct_ibm`.

Per-crossing data (Dirichlet wall values, interface-condition coefficients)
follows a *canonical point shape* ``(n_crossings, *ns_shape)`` — the field
shape with the spatial axes removed and the crossing axis leading.  Any input
NumPy can broadcast to that shape is accepted, mirroring how wall boundary
conditions broadcast over the non-spatial axes; see
`_normalize_point_values`.

The geometric Lagrange coefficients are identical for every *non-spatial
layer* at a given spatial crossing.  The modification of the operator matrix
therefore has a block structure: for crossing ``k`` and non-spatial layer
``j``, the entry :math:`v_{k,j} = A[r_{k,j}, g_{k,j}]` (matrix value at the
ghost column) may differ from layer to layer, and so may the supplied
Dirichlet wall values.  The full-field flat index decomposes as:

.. math::
    \text{flat}(s, j) =
    \underbrace{\sum_i m_s[i] \cdot d[\text{axes}[i]]}_
        {\text{spatial contrib.}}
    + \underbrace{\sum_i m_j[i] \cdot d[\text{ns-axes}[i]]}_
        {\text{ns contrib.}}

where :math:`d[a]` is the C-order stride of axis ``a`` and the two
contributions are **independent** (an outer sum over crossings and ns layers).

## Sign convention

The modified matrix ``M`` and source ``g`` satisfy ``value = M @ c + g``
(source is *added*), matching the gradient/divergence operator convention.
The optional per-row conditioning scale is folded identically into the matrix
and the source.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`IBM`](../symbols/pymrm.ibm.IBM) | class | Consolidated IBM crossing data for both sides of an immersed interface. |
| [`apply_ibm`](../symbols/pymrm.ibm.apply_ibm) | function | Apply the immersed-boundary method to an operator matrix. |
| [`apply_ibm_vector`](../symbols/pymrm.ibm.apply_ibm_vector) | function | Apply the IBM per-row conditioning scale to a flat vector. |
| [`construct_ibm`](../symbols/pymrm.ibm.construct_ibm) | function | Build the immersed-boundary data from a spatial signed-distance field. |

## `IBM()`

[Open dedicated reference page](../symbols/pymrm.ibm.IBM)

Consolidated IBM crossing data for both sides of an immersed interface.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L113-L207)

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

## `apply_ibm(mat, ibm, values_outside = None, values_inside = None, return_bc = 'vector')`

[Open dedicated reference page](../symbols/pymrm.ibm.apply_ibm)

Apply the immersed-boundary method to an operator matrix.

Ghost columns on both sides of the immersed interface are folded into
their respective cut-cell rows in a single call.  The matrix is expanded
from spatial flat indices to full-field flat indices using the ``axes`` /
``shape`` information stored in ``ibm``.

For each wall crossing ``k`` and non-spatial layer ``j``, the matrix
entry ``v = A[full_row(k,j), full_ghost(k,j)]`` is read, and the row is
modified with the same geometric Lagrange coefficients (which are
independent of ``j``).  Wall values may differ per ``j``.

### Parameters

- `mat` (*sparse matrix or array*)
  Operator matrix of shape ``(n_cells, n_cells)`` where
  ``n_cells = ibm.n_cells``.  Converted to CSR internally.

- `ibm` (*IBM*)
  Immersed-boundary data from `construct_ibm`.

- `values_outside` (*array_like, optional*)
  Dirichlet wall values for the *outside* (fluid) cut cells.  ``None``
  (the default) uses the same values as ``values_inside``; if both are
  ``None`` the source is zero.  Otherwise any array broadcastable to the
  canonical point shape ``(n_crossings, *ns_shape)`` is accepted (strict
  NumPy semantics), e.g. a scalar, a ``(nc,)`` per-component array, a
  ``(n_crossings, 1, ..., 1)`` per-crossing array, or the fully specified
  ``(n_crossings, *ns_shape)``.  See `_normalize_point_values`.
  A bare 1-D array of length ``n_crossings`` is only per-crossing for a
  purely spatial field; when non-spatial axes are present reshape it to
  ``(n_crossings, 1, ..., 1)``.

- `values_inside` (*array_like, optional*)
  Dirichlet wall values for the *inside* (solid) cut cells.  Same
  shapes accepted as ``values_outside``.

- `return_bc` (*{'vector', 'matrix'}, optional*)
  ``'vector'`` (default): return the source vector for the supplied
  wall values.  ``'matrix'``: return the pair of sparse source matrices
  ``(G_out, G_in)`` of shape ``(n_cells, n_crossings * ns_size)`` such
  that the source equals
  ``G_out @ values_outside.ravel() + G_in @ values_inside.ravel()``.

### Returns

- `The number of return values depends on *return_bc*:`

- `* ``return_bc='vector'`` → ``(mat_mod, g)``:`
  - ``mat_mod`` : ``scipy.sparse.csr_array``, shape ``(n_cells, n_cells)``
    -- the modified operator matrix;
  - ``g`` : ndarray, shape ``(n_cells,)`` -- the source vector for the
    supplied wall values (``value = mat_mod @ c + g``).

- `* ``return_bc='matrix'`` → ``(mat_mod, G_out, G_in)``:`
  - ``mat_mod`` : as above;
  - ``G_out``, ``G_in`` : ``csr_array``, shape
    ``(n_cells, n_crossings * ns_size)`` -- source matrices with
    ``g = G_out @ values_outside.ravel() + G_in @ values_inside.ravel()``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L867-L1049)

## `apply_ibm_vector(vec, ibm)`

[Open dedicated reference page](../symbols/pymrm.ibm.apply_ibm_vector)

Apply the IBM per-row conditioning scale to a flat vector.

When the operator matrix is constant it is modified once via
`apply_ibm`; any independent right-hand-side term must be scaled
by the same per-row factor to keep the system consistent.  This helper
applies the combined scale for both sides of the interface and expands
from the spatial grid to the full field.

### Parameters

- `vec` (*array_like*)
  Vector to scale, must have ``size == ibm.n_cells``.  May be shaped
  as the full field or passed as a flat array.

- `ibm` (*IBM*)
  Immersed-boundary data from `construct_ibm`.

### Returns

- `numpy.ndarray, shape (n_cells,)`
  Row-scaled vector, always returned as a 1-D flat array.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L1052-L1082)

## `construct_ibm(sdf, x_c, axes = None, shape = None, rescale = True)`

[Open dedicated reference page](../symbols/pymrm.ibm.construct_ibm)

Build the immersed-boundary data from a spatial signed-distance field.

### Parameters

- `sdf` (*array_like*)
  Signed-distance field sampled at the **spatial** cell centres.
  ``sdf.shape`` must equal ``tuple(shape[a] for a in axes)``.
  Cells with ``sdf < 0`` are solid; ``sdf >= 0`` is fluid.

- `x_c` (*array_like or list of array_like*)
  Cell-centre coordinates.  For a 1-D spatial grid a single 1-D array
  is accepted; for N-D spatial grids supply a list of N 1-D arrays (one
  per spatial axis).  The i-th element has length ``sdf.shape[i]``.

- `axes` (*tuple of int, optional*)
  Which axes of the **full field** array correspond to spatial
  coordinates.  Length must equal ``sdf.ndim``.  Defaults to
  ``tuple(range(sdf.ndim))`` (all axes are spatial).

- `shape` (*tuple of int, optional*)
  Full field shape, including any non-spatial dimensions (components,
  phases, species, etc.).  Defaults to ``sdf.shape`` (purely spatial,
  no non-spatial axes).

- `rescale` (*bool, optional*)
  If ``True`` (default), apply a geometric per-row conditioning scale.

### Returns

- `IBM`
  Container holding per-crossing geometry, Lagrange coefficients, and
  per-row conditioning scales for both sides of the interface.

### Notes

The IBM uses cell-centre coordinates directly.  Face coordinates are not
required because the Lagrange interpolation nodes are the cell centres and
the wall position is found from the SDF: ``x_w = x_c + θ (x_ghost − x_c)``.

Every wall crossing ``k`` is the face between one fluid cell and one solid
cell.  ``ibm.coords[k]``, ``ibm.row_out[k]`` (fluid side, spatial flat
index), and ``ibm.row_in[k]`` (solid side, spatial flat index) all refer
to the same physical wall crossing.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L612-L658)
