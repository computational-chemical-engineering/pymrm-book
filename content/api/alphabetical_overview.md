# All Functions and Classes

Alphabetical index of the public PyMRM API with direct links to source-backed reference pages.

| Name | Module | Summary |
| ---- | ------ | ------- |
| [`pymrm.convect.clam`](symbols/pymrm.convect.clam) | `pymrm.convect` | Compute the CLAM TVD correction in normalized-variable space. |
| [`pymrm.convect.construct_convflux_bc`](symbols/pymrm.convect.construct_convflux_bc) | `pymrm.convect` | Construct boundary-face upwind corrections and source terms. |
| [`pymrm.convect.construct_convflux_upwind`](symbols/pymrm.convect.construct_convflux_upwind) | `pymrm.convect` | Construct a first-order upwind convective-flux operator. |
| [`pymrm.convect.construct_convflux_upwind_int`](symbols/pymrm.convect.construct_convflux_upwind_int) | `pymrm.convect` | Construct the internal-face upwind advection operator. |
| [`pymrm.convect.minmod`](symbols/pymrm.convect.minmod) | `pymrm.convect` | Compute the Minmod TVD correction in normalized-variable space. |
| [`pymrm.convect.muscl`](symbols/pymrm.convect.muscl) | `pymrm.convect` | Compute the MUSCL TVD correction in normalized-variable space. |
| [`pymrm.convect.osher`](symbols/pymrm.convect.osher) | `pymrm.convect` | Compute the Osher TVD correction in normalized-variable space. |
| [`pymrm.convect.smart`](symbols/pymrm.convect.smart) | `pymrm.convect` | Compute the SMART TVD correction in normalized-variable space. |
| [`pymrm.convect.stoic`](symbols/pymrm.convect.stoic) | `pymrm.convect` | Compute the STOIC TVD correction in normalized-variable space. |
| [`pymrm.convect.upwind`](symbols/pymrm.convect.upwind) | `pymrm.convect` | Return zero correction (first-order upwind limiter). |
| [`pymrm.convect.vanleer`](symbols/pymrm.convect.vanleer) | `pymrm.convect` | Compute the van-Leer TVD correction in normalized-variable space. |
| [`pymrm.coupling.construct_interface_matrices`](symbols/pymrm.coupling.construct_interface_matrices) | `pymrm.coupling` | Construct implicit interface-coupling matrices for two adjacent domains. |
| [`pymrm.coupling.translate_indices_to_larger_array`](symbols/pymrm.coupling.translate_indices_to_larger_array) | `pymrm.coupling` | Map flat indices from a local array shape to a larger embedding shape. |
| [`pymrm.coupling.update_array_indices`](symbols/pymrm.coupling.update_array_indices) | `pymrm.coupling` | Update sparse-matrix indices for a new embedding shape. |
| [`pymrm.coupling.update_csc_array_indices`](symbols/pymrm.coupling.update_csc_array_indices) | `pymrm.coupling` | Update CSC matrix row/column indexing for embedding in a larger domain. |
| [`pymrm.coupling.update_csr_array_indices`](symbols/pymrm.coupling.update_csr_array_indices) | `pymrm.coupling` | Update CSR matrix row/column indexing for embedding in a larger domain. |
| [`pymrm.grid.generate_grid`](symbols/pymrm.grid.generate_grid) | `pymrm.grid` | Return face coordinates and optionally cell-center coordinates. |
| [`pymrm.grid.non_uniform_grid`](symbols/pymrm.grid.non_uniform_grid) | `pymrm.grid` | Generate a one-dimensional stretched face grid. |
| [`pymrm.helpers.construct_coefficient_matrix`](symbols/pymrm.helpers.construct_coefficient_matrix) | `pymrm.helpers` | Build a sparse coefficient matrix with optional broadcasting and (row, col) coupling. |
| [`pymrm.interpolate.compute_boundary_values`](symbols/pymrm.interpolate.compute_boundary_values) | `pymrm.interpolate` | Compute boundary values and boundary-normal gradients. |
| [`pymrm.interpolate.construct_boundary_value_matrices`](symbols/pymrm.interpolate.construct_boundary_value_matrices) | `pymrm.interpolate` | Build matrices that evaluate boundary values from cell-centered unknowns. |
| [`pymrm.interpolate.create_staggered_array`](symbols/pymrm.interpolate.create_staggered_array) | `pymrm.interpolate` | Create a face/staggered field from scalar, centered, or staggered input. |
| [`pymrm.interpolate.interp_cntr_to_stagg`](symbols/pymrm.interpolate.interp_cntr_to_stagg) | `pymrm.interpolate` | Interpolate cell-centered values to face/staggered locations. |
| [`pymrm.interpolate.interp_cntr_to_stagg_tvd`](symbols/pymrm.interpolate.interp_cntr_to_stagg_tvd) | `pymrm.interpolate` | Perform TVD interpolation from cell centers to faces. |
| [`pymrm.interpolate.interp_stagg_to_cntr`](symbols/pymrm.interpolate.interp_stagg_to_cntr) | `pymrm.interpolate` | Interpolate face/staggered values to cell centers. |
| [`pymrm.numjac.NumJac`](symbols/pymrm.numjac.NumJac) | `pymrm.numjac` | Numerical Jacobian evaluator based on grouped finite differences. |
| [`pymrm.numjac.stencil_block_diagonals`](symbols/pymrm.numjac.stencil_block_diagonals) | `pymrm.numjac` | Generate a block-diagonal or block-banded stencil description. |
| [`pymrm.operators.construct_div`](symbols/pymrm.operators.construct_div) | `pymrm.operators` | Construct a divergence matrix that maps face fluxes to cell balances. |
| [`pymrm.operators.construct_grad`](symbols/pymrm.operators.construct_grad) | `pymrm.operators` | Construct the full gradient operator including boundary contributions. |
| [`pymrm.operators.construct_grad_bc`](symbols/pymrm.operators.construct_grad_bc) | `pymrm.operators` | Construct boundary-face gradient corrections and source terms. |
| [`pymrm.operators.construct_grad_int`](symbols/pymrm.operators.construct_grad_int) | `pymrm.operators` | Construct the interior-face gradient operator. |
| [`pymrm.solve.clip_approach`](symbols/pymrm.solve.clip_approach) | `pymrm.solve` | Project values onto bounds, optionally with a relaxed approach rule. |
| [`pymrm.solve.newton`](symbols/pymrm.solve.newton) | `pymrm.solve` | Solve ``function(x) = 0`` with Newton iterations. |
