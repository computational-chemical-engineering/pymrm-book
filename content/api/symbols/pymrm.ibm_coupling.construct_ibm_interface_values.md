# `pymrm.ibm_coupling.construct_ibm_interface_values`

[Back to module page](../modules/pymrm.ibm_coupling) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`construct_ibm_interface_values(ibm, recon, ic, *, det_tol = 1e-12, return_diagnostics = False)`

## Summary

Eliminate the interface values for linear interface conditions.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_coupling.py#L157-L234)

```python
def construct_ibm_interface_values(ibm, recon, ic, *, det_tol=1e-12,
                                   return_diagnostics=False):
    """Eliminate the interface values for linear interface conditions.

    Substituting the one-sided reconstructions
    ``q_side = alpha_side * c_gamma_side + N_side @ c`` into the two
    interface equations of *ic* gives a 2x2 system per crossing and
    non-spatial layer; its solution expresses the interface values as sparse
    linear functions of the field:

        ``c_gamma_out = H_out @ c + h_out``,
        ``c_gamma_in  = H_in  @ c + h_in``.

    Parameters
    ----------
    ibm : IBM
        Immersed-boundary data from :func:`pymrm.construct_ibm`.
    recon : IBMNormalDerivative
        Reconstruction from
        :func:`pymrm.ibm_recon.construct_ibm_normal_derivative`.
    ic : tuple of dict
        Two interface equations (module docstring).
    det_tol : float, optional
        Relative threshold below which the local 2x2 determinant is treated
        as singular (with a warning naming the crossings).
    return_diagnostics : bool, optional
        Also return a dict with the per-crossing determinant and the
        singular mask.

    Returns
    -------
    H_out, h_out, H_in, h_in
        ``H_*`` are ``csr_array`` of shape ``(n_crossings * ns_size,
        n_cells)``; ``h_*`` are 1-D arrays; rows/entries are ordered
        ``k * ns_size + j`` (matching the ``G_out``/``G_in`` columns of
        :func:`pymrm.apply_ibm`).
    diagnostics : dict, optional
        Only when *return_diagnostics* is true: ``det`` (shape
        ``(n_crossings, ns_size)``) and ``singular`` mask.
    """
    npnt = ibm.n_crossings
    ns = ibm.ns_size
    a, b, d = _ic_coefficients(ic, npnt, ibm.ns_shape)

    alpha_out_full, N_out, alpha_in_full, N_in = \
        construct_ibm_normal_derivative_ops(ibm, recon)
    alpha_out = recon.alpha_out[:, np.newaxis]      # (npnt, 1)
    alpha_in = recon.alpha_in[:, np.newaxis]

    full = (npnt, ns)
    m00 = np.broadcast_to(a[0][0] * alpha_out + b[0][0], full)
    m01 = np.broadcast_to(a[0][1] * alpha_in + b[0][1], full)
    m10 = np.broadcast_to(a[1][0] * alpha_out + b[1][0], full)
    m11 = np.broadcast_to(a[1][1] * alpha_in + b[1][1], full)

    det = m00 * m11 - m01 * m10
    det_inv, singular = _guard_small(det, det_tol, "2x2 elimination matrix")

    minv = ((m11 * det_inv, -m01 * det_inv),
            (-m10 * det_inv, m00 * det_inv))

    def eliminate(row):
        """H and h for the interface value solved from row *row* of M^-1."""
        e_out = np.broadcast_to(
            minv[row][0] * a[0][0] + minv[row][1] * a[1][0], full).ravel()
        e_in = np.broadcast_to(
            minv[row][0] * a[0][1] + minv[row][1] * a[1][1], full).ravel()
        H = (-(_scale_rows(N_out, e_out) + _scale_rows(N_in, e_in))).tocsr()
        h = np.broadcast_to(
            minv[row][0] * d[0] + minv[row][1] * d[1], full).ravel().copy()
        return H, h

    H_out, h_out = eliminate(0)
    H_in, h_in = eliminate(1)

    if return_diagnostics:
        return H_out, h_out, H_in, h_in, {"det": det, "singular": singular}
    return H_out, h_out, H_in, h_in
```
