# All Functions and Classes

An overview of all functions and classes in the `pymrm` package.

| Name | Description |
| ---- | ----------- |
| `pymrm.convect.clam` | Compute the CLAM TVD correction in normalized-variable space. |
| `pymrm.convect.construct_convflux_bc` | Construct boundary-face upwind corrections and source terms. |
| `pymrm.convect.construct_convflux_upwind` | Construct a first-order upwind convective-flux operator. |
| `pymrm.convect.construct_convflux_upwind_int` | Construct the internal-face upwind advection operator. |
| `pymrm.convect.minmod` | Compute the Minmod TVD correction in normalized-variable space. |
| `pymrm.convect.muscl` | Compute the MUSCL TVD correction in normalized-variable space. |
| `pymrm.convect.osher` | Compute the Osher TVD correction in normalized-variable space. |
| `pymrm.convect.smart` | Compute the SMART TVD correction in normalized-variable space. |
| `pymrm.convect.stoic` | Compute the STOIC TVD correction in normalized-variable space. |
| `pymrm.convect.upwind` | Return zero correction (first-order upwind limiter). |
| `pymrm.convect.vanleer` | Compute the van-Leer TVD correction in normalized-variable space. |
| `pymrm.coupling.construct_interface_matrices` | Construct implicit interface-coupling matrices for two adjacent domains. |
| `pymrm.coupling.translate_indices_to_larger_array` | Map flat indices from a local array shape to a larger embedding shape. |
| `pymrm.coupling.update_array_indices` | Update sparse-matrix indices for a new embedding shape. |
| `pymrm.coupling.update_csc_array_indices` | Update CSC matrix row/column indexing for embedding in a larger domain. |
| `pymrm.coupling.update_csr_array_indices` | Update CSR matrix row/column indexing for embedding in a larger domain. |
| `pymrm.grid.generate_grid` | Return face coordinates and optionally cell-center coordinates. |
| `pymrm.grid.non_uniform_grid` | Generate a one-dimensional stretched face grid. |
| `pymrm.helpers.construct_coefficient_matrix` | Build a sparse coefficient matrix with optional broadcasting and (row, col) coupling. |
| `pymrm.interpolate.compute_boundary_values` | Compute boundary values and boundary-normal gradients. |
| `pymrm.interpolate.construct_boundary_value_matrices` | Build matrices that evaluate boundary values from cell-centered unknowns. |
| `pymrm.interpolate.create_staggered_array` | Create a face/staggered field from scalar, centered, or staggered input. |
| `pymrm.interpolate.interp_cntr_to_stagg` | Interpolate cell-centered values to face/staggered locations. |
| `pymrm.interpolate.interp_cntr_to_stagg_tvd` | Perform TVD interpolation from cell centers to faces. |
| `pymrm.interpolate.interp_stagg_to_cntr` | Interpolate face/staggered values to cell centers. |
| `pymrm.numjac.NumJac` | Numerical Jacobian evaluator based on grouped finite differences. |
| `pymrm.numjac.stencil_block_diagonals` | Generate a block-diagonal or block-banded stencil description. |
| `pymrm.operators.construct_div` | Construct a divergence matrix that maps face fluxes to cell balances. |
| `pymrm.operators.construct_grad` | Construct the full gradient operator including boundary contributions. |
| `pymrm.operators.construct_grad_bc` | Construct boundary-face gradient corrections and source terms. |
| `pymrm.operators.construct_grad_int` | Construct the interior-face gradient operator. |
| `pymrm.solve.clip_approach` | Project values onto bounds, optionally with a relaxed approach rule. |
| `pymrm.solve.newton` | Solve ``function(x) = 0`` with Newton iterations. |
