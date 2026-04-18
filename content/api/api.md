# Modules

An overview of all modules of the `pymrm` package.

## [`pymrm.convect`](modules/pymrm.convect.md)

Convective-flux operators and TVD limiter functions.

| Function / Class | Description |
| ---------------- | ----------- |
| [`clam`](symbols/pymrm.convect.clam.md) | Compute the CLAM TVD correction in normalized-variable space. |
| [`construct_convflux_bc`](symbols/pymrm.convect.construct_convflux_bc.md) | Construct boundary-face upwind corrections and source terms. |
| [`construct_convflux_upwind`](symbols/pymrm.convect.construct_convflux_upwind.md) | Construct a first-order upwind convective-flux operator. |
| [`construct_convflux_upwind_int`](symbols/pymrm.convect.construct_convflux_upwind_int.md) | Construct the internal-face upwind advection operator. |
| [`minmod`](symbols/pymrm.convect.minmod.md) | Compute the Minmod TVD correction in normalized-variable space. |
| [`muscl`](symbols/pymrm.convect.muscl.md) | Compute the MUSCL TVD correction in normalized-variable space. |
| [`osher`](symbols/pymrm.convect.osher.md) | Compute the Osher TVD correction in normalized-variable space. |
| [`smart`](symbols/pymrm.convect.smart.md) | Compute the SMART TVD correction in normalized-variable space. |
| [`stoic`](symbols/pymrm.convect.stoic.md) | Compute the STOIC TVD correction in normalized-variable space. |
| [`upwind`](symbols/pymrm.convect.upwind.md) | Return zero correction (first-order upwind limiter). |
| [`vanleer`](symbols/pymrm.convect.vanleer.md) | Compute the van-Leer TVD correction in normalized-variable space. |

## [`pymrm.coupling`](modules/pymrm.coupling.md)

Sparse-matrix utilities for multi-domain coupling and interface assembly.

| Function / Class | Description |
| ---------------- | ----------- |
| [`construct_interface_matrices`](symbols/pymrm.coupling.construct_interface_matrices.md) | Construct implicit interface-coupling matrices for two adjacent domains. |
| [`translate_indices_to_larger_array`](symbols/pymrm.coupling.translate_indices_to_larger_array.md) | Map flat indices from a local array shape to a larger embedding shape. |
| [`update_array_indices`](symbols/pymrm.coupling.update_array_indices.md) | Update sparse-matrix indices for a new embedding shape. |
| [`update_csc_array_indices`](symbols/pymrm.coupling.update_csc_array_indices.md) | Update CSC matrix row/column indexing for embedding in a larger domain. |
| [`update_csr_array_indices`](symbols/pymrm.coupling.update_csr_array_indices.md) | Update CSR matrix row/column indexing for embedding in a larger domain. |

## [`pymrm.grid`](modules/pymrm.grid.md)

Grid-generation utilities for one-dimensional coordinates.

| Function / Class | Description |
| ---------------- | ----------- |
| [`generate_grid`](symbols/pymrm.grid.generate_grid.md) | Return face coordinates and optionally cell-center coordinates. |
| [`non_uniform_grid`](symbols/pymrm.grid.non_uniform_grid.md) | Generate a one-dimensional stretched face grid. |

## [`pymrm.helpers`](modules/pymrm.helpers.md)

pymrm.helpers

| Function / Class | Description |
| ---------------- | ----------- |
| [`construct_coefficient_matrix`](symbols/pymrm.helpers.construct_coefficient_matrix.md) | Build a sparse coefficient matrix with optional broadcasting and (row, col) coupling. |

## [`pymrm.interpolate`](modules/pymrm.interpolate.md)

Interpolation utilities between cell-centered and staggered grids.

| Function / Class | Description |
| ---------------- | ----------- |
| [`compute_boundary_values`](symbols/pymrm.interpolate.compute_boundary_values.md) | Compute boundary values and boundary-normal gradients. |
| [`construct_boundary_value_matrices`](symbols/pymrm.interpolate.construct_boundary_value_matrices.md) | Build matrices that evaluate boundary values from cell-centered unknowns. |
| [`create_staggered_array`](symbols/pymrm.interpolate.create_staggered_array.md) | Create a face/staggered field from scalar, centered, or staggered input. |
| [`interp_cntr_to_stagg`](symbols/pymrm.interpolate.interp_cntr_to_stagg.md) | Interpolate cell-centered values to face/staggered locations. |
| [`interp_cntr_to_stagg_tvd`](symbols/pymrm.interpolate.interp_cntr_to_stagg_tvd.md) | Perform TVD interpolation from cell centers to faces. |
| [`interp_stagg_to_cntr`](symbols/pymrm.interpolate.interp_stagg_to_cntr.md) | Interpolate face/staggered values to cell centers. |

## [`pymrm.numjac`](modules/pymrm.numjac.md)

Numerical Jacobian construction with sparse stencil support.

| Function / Class | Description |
| ---------------- | ----------- |
| [`NumJac`](symbols/pymrm.numjac.NumJac.md) | Numerical Jacobian evaluator based on grouped finite differences. |
| [`stencil_block_diagonals`](symbols/pymrm.numjac.stencil_block_diagonals.md) | Generate a block-diagonal or block-banded stencil description. |

## [`pymrm.operators`](modules/pymrm.operators.md)

Sparse gradient and divergence operators for finite-volume discretisation.

| Function / Class | Description |
| ---------------- | ----------- |
| [`construct_div`](symbols/pymrm.operators.construct_div.md) | Construct a divergence matrix that maps face fluxes to cell balances. |
| [`construct_grad`](symbols/pymrm.operators.construct_grad.md) | Construct the full gradient operator including boundary contributions. |
| [`construct_grad_bc`](symbols/pymrm.operators.construct_grad_bc.md) | Construct boundary-face gradient corrections and source terms. |
| [`construct_grad_int`](symbols/pymrm.operators.construct_grad_int.md) | Construct the interior-face gradient operator. |

## [`pymrm.solve`](modules/pymrm.solve.md)

Nonlinear-solver utilities used by `pymrm`.

| Function / Class | Description |
| ---------------- | ----------- |
| [`clip_approach`](symbols/pymrm.solve.clip_approach.md) | Project values onto bounds, optionally with a relaxed approach rule. |
| [`newton`](symbols/pymrm.solve.newton.md) | Solve ``function(x) = 0`` with Newton iterations. |

