# `pymrm.ibm_coupling`

[Back to modules overview](../api)

General interface conditions at immersed boundaries for `pymrm`.

This module provides *Layer 2* of the generalized immersed-interface
coupling: it combines the one-sided normal-derivative reconstructions of
`pymrm.ibm_recon` with interface conditions specified in the same
dictionary format as `pymrm.coupling.construct_interface_matrices`,
and eliminates the two unknown interface values per crossing.

## Interface conditions

``ic`` is a tuple of two equation dictionaries.  Each dictionary defines one
interface equation

.. math::
    a_\text{out}\, q_\text{out} + a_\text{in}\, q_\text{in}
    + b_\text{out}\, c_\Gamma^\text{out} + b_\text{in}\, c_\Gamma^\text{in}
    = d ,

with ``{"a": (a_out, a_in), "b": (b_out, b_in), "d": d}`` and the *outward
per side* derivative convention of `pymrm.ibm_recon` (``q_out`` out of
the fluid, ``q_in`` out of the solid).  With this convention the dictionaries
are numerically identical to a grid-aligned
`~pymrm.coupling.construct_interface_matrices` call with the fluid as
subdomain 0.  Examples:

conjugate diffusion (flux + value continuity)::

    ic = ({"a": (D_out, D_in), "b": (0, 0), "d": 0},
          {"a": (0, 0), "b": (1, -1), "d": 0})

partition coefficient ``c_out = K c_in``::

    ic = ({"a": (D_out, D_in), "b": (0, 0), "d": 0},
          {"a": (0, 0), "b": (1, -K), "d": 0})

Coefficient broadcasting follows the canonical point shape
``(n_crossings, *ns_shape)`` with strict NumPy semantics (see
`pymrm.ibm._normalize_point_values`): a scalar applies everywhere, a
``(nc,)`` array is per component, ``(n_crossings, 1, ..., 1)`` is per crossing,
and any array broadcastable to ``(n_crossings, *ns_shape)`` is accepted.  A
bare 1-D array of length ``n_crossings`` is per-crossing only for a purely
spatial field; when non-spatial axes are present reshape it to
``(n_crossings, 1, ..., 1)``.  The per-crossing/per-component 2x2 eliminations
are independent, so this linear path cannot couple components at the interface;
cross-component interface physics (Maxwell-Stefan, coupled surface reactions)
uses the augmented degree-of-freedom framework built on
`pymrm.ibm_recon.construct_ibm_normal_derivative_ops`.

## Usage

The elimination expresses the interface values as sparse functions of the
field, ``c_gamma = H @ c + h``, which enter through the source matrices of
`pymrm.apply_ibm`::

    ibm = construct_ibm(sdf, x_c)
    recon = construct_ibm_normal_derivative(ibm, sdf, x_c)
    A_final, g_final = apply_ibm_interface(A, ibm, recon, ic)
    # solve A_final @ c + g_final == rhs terms as usual (source is *added*)

Row conditioning from `pymrm.construct_ibm` is handled automatically:
``H``/``h`` describe wall values in terms of the unscaled field and enter
only through the already-scaled ``G`` matrices.  Any independent right-hand
side assembled before the IBM must still pass through
`pymrm.apply_ibm_vector`, exactly as for the Dirichlet IBM.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_coupling.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`apply_ibm_interface`](../symbols/pymrm.ibm_coupling.apply_ibm_interface) | function | Apply general linear interface conditions to an operator matrix. |
| [`construct_ibm_boundary_values`](../symbols/pymrm.ibm_coupling.construct_ibm_boundary_values) | function | Eliminate the interface value of a single side (immersed Robin BC). |
| [`construct_ibm_interface_values`](../symbols/pymrm.ibm_coupling.construct_ibm_interface_values) | function | Eliminate the interface values for linear interface conditions. |

## `apply_ibm_interface(mat, ibm, recon, ic, *, det_tol = 1e-12, return_values = False)`

[Open dedicated reference page](../symbols/pymrm.ibm_coupling.apply_ibm_interface)

Apply general linear interface conditions to an operator matrix.

Combines `pymrm.apply_ibm` (ghost-column folding, source matrices)
with the interface-value elimination of
`construct_ibm_interface_values`:

    ``A_final = A_ibm + G_out @ H_out + G_in @ H_in``
    ``g_final = G_out @ h_out + G_in @ h_in``

### Parameters

- `mat` (*sparse matrix or array*)
  Operator matrix of shape ``(n_cells, n_cells)``.

- `ibm` (*IBM*)

- `recon` (*IBMNormalDerivative*)

- `ic` (*tuple of dict*)
  Two interface equations (module docstring).

- `det_tol` (*float, optional*)
  Passed to `construct_ibm_interface_values`.

- `return_values` (*bool, optional*)
  Also return ``(H_out, h_out, H_in, h_in)`` for post-processing wall
  values and fluxes.

### Returns

- `A_final` (*csr_array*)
  Modified operator matrix.

- `g_final` (*ndarray, shape (n_cells,)*)
  Interface source (sign convention: *added*, ``value = A @ c + g``).

- `values` (*tuple, optional*)
  Only when *return_values* is true.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_coupling.py#L237-L279)

## `construct_ibm_boundary_values(ibm, recon, bc, side = 'out', *, det_tol = 1e-12)`

[Open dedicated reference page](../symbols/pymrm.ibm_coupling.construct_ibm_boundary_values)

Eliminate the interface value of a single side (immersed Robin BC).

For a boundary condition on one side only,

    ``a * q_side + b * c_gamma_side = d``

(outward derivative of that side), the interface value becomes

    ``c_gamma_side = H @ c + h``.

This covers immersed Neumann/Robin walls where the other region is not
modelled: pass the returned ``H``/``h`` for this side to the assembly and
handle the other side as a plain Dirichlet value through
`pymrm.apply_ibm`, e.g. ::

    A_ibm, G_out, G_in = apply_ibm(A, ibm, return_bc="matrix")
    H, h = construct_ibm_boundary_values(ibm, recon, bc, side="out")
    A_final = (A_ibm + G_out @ H).tocsr()
    g_final = G_out @ h        # solid side: G_in @ values as usual

### Parameters

- `ibm` (*IBM*)

- `recon` (*IBMNormalDerivative*)

- `bc` (*dict*)
  Single equation ``{"a": ..., "b": ..., "d": ...}`` (same coefficient
  broadcasting rules as *ic*, but no side pairs).

- `side` (*{'out', 'in'}, optional*)
  Which side of the interface the condition applies to.

- `det_tol` (*float, optional*)
  Relative threshold for the local denominator ``a * alpha + b``.

### Returns

- `H` (*csr_array, shape (n_crossings * ns_size, n_cells)*)

- `h` (*ndarray, shape (n_crossings * ns_size,)*)

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_coupling.py#L282-L342)

## `construct_ibm_interface_values(ibm, recon, ic, *, det_tol = 1e-12, return_diagnostics = False)`

[Open dedicated reference page](../symbols/pymrm.ibm_coupling.construct_ibm_interface_values)

Eliminate the interface values for linear interface conditions.

Substituting the one-sided reconstructions
``q_side = alpha_side * c_gamma_side + N_side @ c`` into the two
interface equations of *ic* gives a 2x2 system per crossing and
non-spatial layer; its solution expresses the interface values as sparse
linear functions of the field:

    ``c_gamma_out = H_out @ c + h_out``,
    ``c_gamma_in  = H_in  @ c + h_in``.

### Parameters

- `ibm` (*IBM*)
  Immersed-boundary data from `pymrm.construct_ibm`.

- `recon` (*IBMNormalDerivative*)
  Reconstruction from
  `pymrm.ibm_recon.construct_ibm_normal_derivative`.

- `ic` (*tuple of dict*)
  Two interface equations (module docstring).

- `det_tol` (*float, optional*)
  Relative threshold below which the local 2x2 determinant is treated
  as singular (with a warning naming the crossings).

- `return_diagnostics` (*bool, optional*)
  Also return a dict with the per-crossing determinant and the
  singular mask.

### Returns

- `H_out, h_out, H_in, h_in`
  ``H_*`` are ``csr_array`` of shape ``(n_crossings * ns_size,
  n_cells)``; ``h_*`` are 1-D arrays; rows/entries are ordered
  ``k * ns_size + j`` (matching the ``G_out``/``G_in`` columns of
  `pymrm.apply_ibm`).

- `diagnostics` (*dict, optional*)
  Only when *return_diagnostics* is true: ``det`` (shape
  ``(n_crossings, ns_size)``) and ``singular`` mask.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_coupling.py#L157-L234)
