# Modules

An overview of all modules of the `pymrm` package.

## `pymrm.convect`

Convective-flux operators and TVD limiter functions.

| Function / Class | Description |
| ---------------- | ----------- |
| `clam` | Compute the CLAM TVD correction in normalized-variable space. |
| `construct_convflux_bc` | Construct boundary-face upwind corrections and source terms. |
| `construct_convflux_upwind` | Construct a first-order upwind convective-flux operator. |
| `construct_convflux_upwind_int` | Construct the internal-face upwind advection operator. |
| `minmod` | Compute the Minmod TVD correction in normalized-variable space. |
| `muscl` | Compute the MUSCL TVD correction in normalized-variable space. |
| `osher` | Compute the Osher TVD correction in normalized-variable space. |
| `smart` | Compute the SMART TVD correction in normalized-variable space. |
| `stoic` | Compute the STOIC TVD correction in normalized-variable space. |
| `upwind` | Return zero correction (first-order upwind limiter). |
| `vanleer` | Compute the van-Leer TVD correction in normalized-variable space. |

## `pymrm.coupling`

Sparse-matrix utilities for multi-domain coupling and interface assembly.

| Function / Class | Description |
| ---------------- | ----------- |
| `construct_interface_matrices` | Construct implicit interface-coupling matrices for two adjacent domains. |
| `translate_indices_to_larger_array` | Map flat indices from a local array shape to a larger embedding shape. |
| `update_array_indices` | Update sparse-matrix indices for a new embedding shape. |
| `update_csc_array_indices` | Update CSC matrix row/column indexing for embedding in a larger domain. |
| `update_csr_array_indices` | Update CSR matrix row/column indexing for embedding in a larger domain. |

## `pymrm.grid`

Grid-generation utilities for one-dimensional coordinates.

| Function / Class | Description |
| ---------------- | ----------- |
| `generate_grid` | Return face coordinates and optionally cell-center coordinates. |
| `non_uniform_grid` | Generate a one-dimensional stretched face grid. |

## `pymrm.helpers`

pymrm.helpers

| Function / Class | Description |
| ---------------- | ----------- |
| `construct_coefficient_matrix` | Build a sparse coefficient matrix with optional broadcasting and (row, col) coupling. |

## `pymrm.interpolate`

Interpolation utilities between cell-centered and staggered grids.

| Function / Class | Description |
| ---------------- | ----------- |
| `compute_boundary_values` | Compute boundary values and boundary-normal gradients. |
| `construct_boundary_value_matrices` | Build matrices that evaluate boundary values from cell-centered unknowns. |
| `create_staggered_array` | Create a face/staggered field from scalar, centered, or staggered input. |
| `interp_cntr_to_stagg` | Interpolate cell-centered values to face/staggered locations. |
| `interp_cntr_to_stagg_tvd` | Perform TVD interpolation from cell centers to faces. |
| `interp_stagg_to_cntr` | Interpolate face/staggered values to cell centers. |

## `pymrm.numjac`

Numerical Jacobian construction with sparse stencil support.

| Function / Class | Description |
| ---------------- | ----------- |
| `NumJac` | Numerical Jacobian evaluator based on grouped finite differences. |
| `stencil_block_diagonals` | Generate a block-diagonal or block-banded stencil description. |

## `pymrm.operators`

Sparse gradient and divergence operators for finite-volume discretisation.

| Function / Class | Description |
| ---------------- | ----------- |
| `construct_div` | Construct a divergence matrix that maps face fluxes to cell balances. |
| `construct_grad` | Construct the full gradient operator including boundary contributions. |
| `construct_grad_bc` | Construct boundary-face gradient corrections and source terms. |
| `construct_grad_int` | Construct the interior-face gradient operator. |

## `pymrm.solve`

Nonlinear-solver utilities used by :mod:`pymrm`.

| Function / Class | Description |
| ---------------- | ----------- |
| `clip_approach` | Project values onto bounds, optionally with a relaxed approach rule. |
| `newton` | Solve ``function(x) = 0`` with Newton iterations. |

