# `pymrm.ibm_coupling.apply_ibm_interface`

[Back to module page](../modules/pymrm.ibm_coupling) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`apply_ibm_interface(mat, ibm, recon, ic, *, det_tol = 1e-12, return_values = False)`

## Summary

Apply general linear interface conditions to an operator matrix.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_coupling.py#L237-L279)

```python
def apply_ibm_interface(mat, ibm, recon, ic, *, det_tol=1e-12,
                        return_values=False):
    """Apply general linear interface conditions to an operator matrix.

    Combines :func:`pymrm.apply_ibm` (ghost-column folding, source matrices)
    with the interface-value elimination of
    :func:`construct_ibm_interface_values`:

        ``A_final = A_ibm + G_out @ H_out + G_in @ H_in``
        ``g_final = G_out @ h_out + G_in @ h_in``

    Parameters
    ----------
    mat : sparse matrix or array
        Operator matrix of shape ``(n_cells, n_cells)``.
    ibm : IBM
    recon : IBMNormalDerivative
    ic : tuple of dict
        Two interface equations (module docstring).
    det_tol : float, optional
        Passed to :func:`construct_ibm_interface_values`.
    return_values : bool, optional
        Also return ``(H_out, h_out, H_in, h_in)`` for post-processing wall
        values and fluxes.

    Returns
    -------
    A_final : csr_array
        Modified operator matrix.
    g_final : ndarray, shape (n_cells,)
        Interface source (sign convention: *added*, ``value = A @ c + g``).
    values : tuple, optional
        Only when *return_values* is true.
    """
    A_ibm, G_out, G_in = apply_ibm(mat, ibm, return_bc="matrix")
    H_out, h_out, H_in, h_in = construct_ibm_interface_values(
        ibm, recon, ic, det_tol=det_tol)
    A_final = (A_ibm + G_out @ H_out + G_in @ H_in).tocsr()
    g_final = (np.asarray(G_out @ h_out).ravel()
               + np.asarray(G_in @ h_in).ravel())
    if return_values:
        return A_final, g_final, (H_out, h_out, H_in, h_in)
    return A_final, g_final
```
