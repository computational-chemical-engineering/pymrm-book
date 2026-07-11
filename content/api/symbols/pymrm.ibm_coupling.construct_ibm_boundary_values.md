# `pymrm.ibm_coupling.construct_ibm_boundary_values`

[Back to module page](../modules/pymrm.ibm_coupling) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`construct_ibm_boundary_values(ibm, recon, bc, side = 'out', *, det_tol = 1e-12)`

## Summary

Eliminate the interface value of a single side (immersed Robin BC).

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_coupling.py#L282-L342)

```python
def construct_ibm_boundary_values(ibm, recon, bc, side="out", *,
                                  det_tol=1e-12):
    """Eliminate the interface value of a single side (immersed Robin BC).

    For a boundary condition on one side only,

        ``a * q_side + b * c_gamma_side = d``

    (outward derivative of that side), the interface value becomes

        ``c_gamma_side = H @ c + h``.

    This covers immersed Neumann/Robin walls where the other region is not
    modelled: pass the returned ``H``/``h`` for this side to the assembly and
    handle the other side as a plain Dirichlet value through
    :func:`pymrm.apply_ibm`, e.g. ::

        A_ibm, G_out, G_in = apply_ibm(A, ibm, return_bc="matrix")
        H, h = construct_ibm_boundary_values(ibm, recon, bc, side="out")
        A_final = (A_ibm + G_out @ H).tocsr()
        g_final = G_out @ h        # solid side: G_in @ values as usual

    Parameters
    ----------
    ibm : IBM
    recon : IBMNormalDerivative
    bc : dict
        Single equation ``{"a": ..., "b": ..., "d": ...}`` (same coefficient
        broadcasting rules as *ic*, but no side pairs).
    side : {'out', 'in'}, optional
        Which side of the interface the condition applies to.
    det_tol : float, optional
        Relative threshold for the local denominator ``a * alpha + b``.

    Returns
    -------
    H : csr_array, shape (n_crossings * ns_size, n_cells)
    h : ndarray, shape (n_crossings * ns_size,)
    """
    npnt = ibm.n_crossings
    ns = ibm.ns_size
    if side not in ("out", "in"):
        raise ValueError(f"side must be 'out' or 'in', got {side!r}")

    a = _coerce_coeff(bc.get("a", 0.0), npnt, ibm.ns_shape, "bc['a']")
    b = _coerce_coeff(bc.get("b", 0.0), npnt, ibm.ns_shape, "bc['b']")
    d = _coerce_coeff(bc.get("d", 0.0), npnt, ibm.ns_shape, "bc['d']")

    ops = construct_ibm_normal_derivative_ops(ibm, recon)
    if side == "out":
        alpha, N = recon.alpha_out[:, np.newaxis], ops[1]
    else:
        alpha, N = recon.alpha_in[:, np.newaxis], ops[3]

    full = (npnt, ns)
    den = np.broadcast_to(a * alpha + b, full)
    den_inv, _ = _guard_small(den, det_tol, "boundary-condition denominator")

    H = -_scale_rows(N, np.broadcast_to(a * den_inv, full).ravel())
    h = np.broadcast_to(d * den_inv, full).ravel().copy()
    return H.tocsr(), h
```
