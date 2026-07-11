# `pymrm.ibm.apply_ibm`

[Back to module page](../modules/pymrm.ibm) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`apply_ibm(mat, ibm, values_outside = None, values_inside = None, return_bc = 'vector')`

## Summary

Apply the immersed-boundary method to an operator matrix.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm.py#L867-L1049)

```python
def apply_ibm(mat, ibm, values_outside=None, values_inside=None,
              return_bc="vector"):
    """Apply the immersed-boundary method to an operator matrix.

    Ghost columns on both sides of the immersed interface are folded into
    their respective cut-cell rows in a single call.  The matrix is expanded
    from spatial flat indices to full-field flat indices using the ``axes`` /
    ``shape`` information stored in ``ibm``.

    For each wall crossing ``k`` and non-spatial layer ``j``, the matrix
    entry ``v = A[full_row(k,j), full_ghost(k,j)]`` is read, and the row is
    modified with the same geometric Lagrange coefficients (which are
    independent of ``j``).  Wall values may differ per ``j``.

    Parameters
    ----------
    mat : sparse matrix or array
        Operator matrix of shape ``(n_cells, n_cells)`` where
        ``n_cells = ibm.n_cells``.  Converted to CSR internally.
    ibm : IBM
        Immersed-boundary data from :func:`construct_ibm`.
    values_outside : array_like, optional
        Dirichlet wall values for the *outside* (fluid) cut cells.  ``None``
        (the default) uses the same values as ``values_inside``; if both are
        ``None`` the source is zero.  Otherwise any array broadcastable to the
        canonical point shape ``(n_crossings, *ns_shape)`` is accepted (strict
        NumPy semantics), e.g. a scalar, a ``(nc,)`` per-component array, a
        ``(n_crossings, 1, ..., 1)`` per-crossing array, or the fully specified
        ``(n_crossings, *ns_shape)``.  See :func:`_normalize_point_values`.
        A bare 1-D array of length ``n_crossings`` is only per-crossing for a
        purely spatial field; when non-spatial axes are present reshape it to
        ``(n_crossings, 1, ..., 1)``.
    values_inside : array_like, optional
        Dirichlet wall values for the *inside* (solid) cut cells.  Same
        shapes accepted as ``values_outside``.
    return_bc : {'vector', 'matrix'}, optional
        ``'vector'`` (default): return the source vector for the supplied
        wall values.  ``'matrix'``: return the pair of sparse source matrices
        ``(G_out, G_in)`` of shape ``(n_cells, n_crossings * ns_size)`` such
        that the source equals
        ``G_out @ values_outside.ravel() + G_in @ values_inside.ravel()``.

    Returns
    -------
    The number of return values depends on *return_bc*:

    * ``return_bc='vector'`` → ``(mat_mod, g)``:

      - ``mat_mod`` : ``scipy.sparse.csr_array``, shape ``(n_cells, n_cells)``
        -- the modified operator matrix;
      - ``g`` : ndarray, shape ``(n_cells,)`` -- the source vector for the
        supplied wall values (``value = mat_mod @ c + g``).

    * ``return_bc='matrix'`` → ``(mat_mod, G_out, G_in)``:

      - ``mat_mod`` : as above;
      - ``G_out``, ``G_in`` : ``csr_array``, shape
        ``(n_cells, n_crossings * ns_size)`` -- source matrices with
        ``g = G_out @ values_outside.ravel() + G_in @ values_inside.ravel()``.
    """
    n_full = ibm.n_cells
    ns = ibm.ns_size
    npnt = ibm.n_crossings

    val_out, val_in = _normalize_values(values_outside, values_inside, npnt,
                                        ibm.ns_shape)

    A = csr_array(mat)

    # --- Full flat index expansion ---
    pure_spatial = _is_pure_spatial(ibm)
    ns_c = _ns_contributions(ibm.shape, ibm.axes)  # (ns,)

    def expand(spatial_flat):
        """Spatial flat → full flat matrix of shape (len, ns)."""
        if pure_spatial:
            return np.asarray(spatial_flat, dtype=np.intp)[:, np.newaxis]
        sc = _spatial_contributions(spatial_flat, ibm.shape, ibm.axes)
        return sc[:, np.newaxis] + ns_c[np.newaxis, :]

    f_row_out = expand(ibm.row_out)       # (npnt, ns)
    f_ghost_out = expand(ibm.ghost_out)   # (npnt, ns)
    f_row_in = expand(ibm.row_in)
    f_ghost_in = expand(ibm.ghost_in)

    has_opp_out = ibm.opp_out >= 0        # (npnt,)
    f_opp_out = expand(np.where(has_opp_out, ibm.opp_out, ibm.row_out))
    has_opp_in = ibm.opp_in >= 0
    f_opp_in = expand(np.where(has_opp_in, ibm.opp_in, ibm.row_in))

    # --- Read ghost matrix entries: v[k, j] = A[row(k,j), ghost(k,j)] ---
    v_out = _read_entries(A, f_row_out.ravel(), f_ghost_out.ravel()).reshape(npnt, ns)
    v_in = _read_entries(A, f_row_in.ravel(), f_ghost_in.ravel()).reshape(npnt, ns)

    def bc_coef(arr):
        """Broadcast 1-D per-crossing array to (npnt, ns) view."""
        return np.broadcast_to(arr[:, np.newaxis], (npnt, ns))

    # --- Matrix correction (COO) ---
    has_opp_out_2d = has_opp_out[:, np.newaxis].repeat(ns, axis=1)  # (npnt, ns) bool
    has_opp_in_2d = has_opp_in[:, np.newaxis].repeat(ns, axis=1)

    cr_out_flat = f_row_out.ravel()
    fg_out_flat = f_ghost_out.ravel()
    fo_out_mask = has_opp_out_2d.ravel()
    cr_in_flat = f_row_in.ravel()
    fg_in_flat = f_ghost_in.ravel()
    fo_in_mask = has_opp_in_2d.ravel()

    cr_out = np.concatenate([cr_out_flat,
                              cr_out_flat[fo_out_mask],
                              cr_out_flat])
    cc_out = np.concatenate([cr_out_flat,                          # diagonal
                              f_opp_out.ravel()[fo_out_mask],      # opposite
                              fg_out_flat])                         # ghost removal
    cd_out = np.concatenate([(v_out * bc_coef(ibm.coef_c_out)).ravel(),
                              (v_out * bc_coef(ibm.coef_o_out)).ravel()[fo_out_mask],
                              -v_out.ravel()])

    cr_in = np.concatenate([cr_in_flat,
                             cr_in_flat[fo_in_mask],
                             cr_in_flat])
    cc_in = np.concatenate([cr_in_flat,
                             f_opp_in.ravel()[fo_in_mask],
                             fg_in_flat])
    cd_in = np.concatenate([(v_in * bc_coef(ibm.coef_c_in)).ravel(),
                              (v_in * bc_coef(ibm.coef_o_in)).ravel()[fo_in_mask],
                              -v_in.ravel()])

    correction = coo_array(
        (np.concatenate([cd_out, cd_in]),
         (np.concatenate([cr_out, cr_in]),
          np.concatenate([cc_out, cc_in]))),
        shape=(n_full, n_full),
    )
    mat_mod = (A + correction.tocsr()).tocsr()

    # --- Row scaling (only cut-cell rows differ from unity) ---
    scale_rows, scale_vals = _combined_cut_scale(ibm)
    _scale_csr_rows(mat_mod, scale_rows, scale_vals)

    # --- Source matrices G_out and G_in, shape (n_full, npnt * ns) ---
    n_cols = npnt * ns
    # Column index for crossing k and ns layer j: k*ns + j
    k_rep = np.repeat(np.arange(npnt, dtype=np.intp), ns)   # (npnt*ns,)
    j_tile = np.tile(np.arange(ns, dtype=np.intp), npnt)    # (npnt*ns,)
    own_col = k_rep * ns + j_tile                            # (npnt*ns,)

    has_sib_out_flat = np.repeat(ibm.sib_out >= 0, ns)      # (npnt*ns,)
    sib_out_col = (np.where(has_sib_out_flat, np.repeat(ibm.sib_out, ns), 0) * ns + j_tile)
    has_sib_in_flat = np.repeat(ibm.sib_in >= 0, ns)
    sib_in_col = (np.where(has_sib_in_flat, np.repeat(ibm.sib_in, ns), 0) * ns + j_tile)

    G_out = coo_array(
        (np.concatenate([(v_out * bc_coef(ibm.coef_w_out)).ravel(),
                          (v_out * bc_coef(ibm.coef_w_sib_out)).ravel()[has_sib_out_flat]]),
         (np.concatenate([f_row_out.ravel(),
                           f_row_out.ravel()[has_sib_out_flat]]),
          np.concatenate([own_col,
                           sib_out_col[has_sib_out_flat]]))),
        shape=(n_full, n_cols),
    ).tocsr()

    G_in = coo_array(
        (np.concatenate([(v_in * bc_coef(ibm.coef_w_in)).ravel(),
                          (v_in * bc_coef(ibm.coef_w_sib_in)).ravel()[has_sib_in_flat]]),
         (np.concatenate([f_row_in.ravel(),
                           f_row_in.ravel()[has_sib_in_flat]]),
          np.concatenate([own_col,
                           sib_in_col[has_sib_in_flat]]))),
        shape=(n_full, n_cols),
    ).tocsr()

    _scale_csr_rows(G_out, scale_rows, scale_vals)
    _scale_csr_rows(G_in, scale_rows, scale_vals)

    if return_bc == "matrix":
        return mat_mod, G_out, G_in
    if return_bc == "vector":
        g = (np.asarray(G_out @ val_out.ravel()).ravel()
             + np.asarray(G_in @ val_in.ravel()).ravel())
        return mat_mod, g
    raise ValueError(f"return_bc must be 'vector' or 'matrix', got {return_bc!r}")
```
