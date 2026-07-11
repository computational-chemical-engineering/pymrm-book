# `pymrm.ibm_recon.gfd_normal_derivative_weights`

[Back to module page](../modules/pymrm.ibm_recon) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`gfd_normal_derivative_weights(x_gamma, x_cells, direction, degree = 2, hvec = None, weight_power = 4, interface_penalty = 1.0)`

## Summary

GFD weights for a directional derivative at a single interface point.

## Documentation

Returns ``alpha``, ``gamma`` and diagnostics such that

    ``dc/du|_Gamma ~= alpha * c_gamma + gamma @ c_cells``

is exact for all polynomials up to *degree*.  This is the single-point
convenience form of the batched kernel used by
`construct_ibm_normal_derivative`; *direction* is the (not necessarily
unit) derivative direction ``u``.

### Parameters

- `x_gamma` (*array_like, shape (ndim,)*)
  Interface point.

- `x_cells` (*array_like, shape (N, ndim)*)
  Same-side cell centres.

- `direction` (*array_like, shape (ndim,)*)
  Derivative direction; normalized internally.

- `degree` (*int, optional*)
  Polynomial exactness degree (default 2).

- `hvec` (*array_like, shape (ndim,), optional*)
  Per-axis coordinate scaling.  Defaults to the median point distance.

- `weight_power` (*float, optional*)
  Distance-penalty exponent: ``q_i = 1 + r_i**weight_power`` in scaled
  coordinates (default 4).

- `interface_penalty` (*float, optional*)
  Minimum-norm weight of the interface node (default 1.0).

### Returns

- `alpha` (*float*)
  Weight of the interface value.

- `gamma` (*ndarray, shape (N,)*)
  Weights of the cell values.

- `info` (*dict*)
  ``cond`` and ``moment_residual`` diagnostics.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/63f4e25920919f682a5b9ba06edd0f8453c62a65/src/pymrm/ibm_recon.py#L244-L307)

```python
def gfd_normal_derivative_weights(x_gamma, x_cells, direction, degree=2,
                                  hvec=None, weight_power=4,
                                  interface_penalty=1.0):
    """GFD weights for a directional derivative at a single interface point.

    Returns ``alpha``, ``gamma`` and diagnostics such that

        ``dc/du|_Gamma ~= alpha * c_gamma + gamma @ c_cells``

    is exact for all polynomials up to *degree*.  This is the single-point
    convenience form of the batched kernel used by
    :func:`construct_ibm_normal_derivative`; *direction* is the (not necessarily
    unit) derivative direction ``u``.

    Parameters
    ----------
    x_gamma : array_like, shape (ndim,)
        Interface point.
    x_cells : array_like, shape (N, ndim)
        Same-side cell centres.
    direction : array_like, shape (ndim,)
        Derivative direction; normalized internally.
    degree : int, optional
        Polynomial exactness degree (default 2).
    hvec : array_like, shape (ndim,), optional
        Per-axis coordinate scaling.  Defaults to the median point distance.
    weight_power : float, optional
        Distance-penalty exponent: ``q_i = 1 + r_i**weight_power`` in scaled
        coordinates (default 4).
    interface_penalty : float, optional
        Minimum-norm weight of the interface node (default 1.0).

    Returns
    -------
    alpha : float
        Weight of the interface value.
    gamma : ndarray, shape (N,)
        Weights of the cell values.
    info : dict
        ``cond`` and ``moment_residual`` diagnostics.
    """
    x_gamma = np.asarray(x_gamma, dtype=float).ravel()
    x_cells = np.atleast_2d(np.asarray(x_cells, dtype=float))
    u = np.asarray(direction, dtype=float).ravel()
    u = u / np.linalg.norm(u)
    dim = x_gamma.size

    if hvec is None:
        r = np.linalg.norm(x_cells - x_gamma, axis=1)
        h = np.median(r[r > 0]) if np.any(r > 0) else 1.0
        hvec = np.full(dim, h)
    else:
        hvec = np.asarray(hvec, dtype=float).ravel()

    Y = np.vstack([np.zeros(dim), (x_cells - x_gamma) / hvec])[None, :, :]
    r = np.linalg.norm(Y[0], axis=1)
    q = 1.0 + r ** weight_power
    q[0] = interface_penalty
    qinv = (1.0 / q)[None, :]
    u_scaled = (u / hvec)[None, :]

    a, cond, moment_res = _gfd_weights_batched(Y, qinv, u_scaled, degree)
    info = {"cond": float(cond[0]), "moment_residual": float(moment_res[0])}
    return float(a[0, 0]), a[0, 1:], info
```
