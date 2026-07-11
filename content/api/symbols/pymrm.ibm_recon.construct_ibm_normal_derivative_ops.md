# `pymrm.ibm_recon.construct_ibm_normal_derivative_ops`

[Back to module page](../modules/pymrm.ibm_recon) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`construct_ibm_normal_derivative_ops(ibm, recon)`

## Summary

Expand the reconstruction operators to the full field layout.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L762-L804)

```python
def construct_ibm_normal_derivative_ops(ibm, recon):
    """Expand the reconstruction operators to the full field layout.

    Returns operators acting on the *flattened full field* ``c`` (including
    non-spatial axes) with rows ordered ``k * ns_size + j`` for crossing ``k``
    and non-spatial layer ``j`` — the same column ordering used by the
    ``G_out``/``G_in`` source matrices of :func:`pymrm.apply_ibm`:

        ``q_side.ravel() = alpha_side_full * w_side + N_side @ c.ravel()``

    Parameters
    ----------
    ibm : IBM
    recon : IBMNormalDerivative

    Returns
    -------
    alpha_out_full : ndarray, shape (n_crossings * ns_size,)
    N_out : csr_array, shape (n_crossings * ns_size, n_cells)
    alpha_in_full : ndarray, shape (n_crossings * ns_size,)
    N_in : csr_array, shape (n_crossings * ns_size, n_cells)
    """
    ns = ibm.ns_size
    npnt = ibm.n_crossings

    def expand(D):
        if _is_pure_spatial(ibm):
            return csr_array(D.copy())
        coo = D.tocoo()
        sc = _spatial_contributions(coo.col, ibm.shape, ibm.axes)
        ns_c = _ns_contributions(ibm.shape, ibm.axes)
        rows = (coo.row.astype(np.intp) * ns)[:, np.newaxis] \
            + np.arange(ns, dtype=np.intp)[np.newaxis, :]
        cols = sc[:, np.newaxis] + ns_c[np.newaxis, :]
        data = np.broadcast_to(coo.data[:, np.newaxis], rows.shape)
        return coo_array(
            (data.ravel(), (rows.ravel(), cols.ravel())),
            shape=(npnt * ns, ibm.n_cells),
        ).tocsr()

    alpha_out_full = np.repeat(recon.alpha_out, ns)
    alpha_in_full = np.repeat(recon.alpha_in, ns)
    return alpha_out_full, expand(recon.D_out), alpha_in_full, expand(recon.D_in)
```
