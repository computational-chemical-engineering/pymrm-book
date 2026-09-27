# `pymrm.checks.residual_check`

[Back to module page](../modules/pymrm.checks) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`residual_check(fun, x, tol = 1e-08)`

## Summary

Judge a solution by its componentwise backward error.

## Documentation

An absolute threshold on the residual depends on the units and scaling of
the equations. The backward error ``max_i |g_i| / (|J| |x| + |J x - g|)_i``
is scale-free: it measures the relative change in the (linearised) equation
coefficients that would make ``x`` exact.

### Parameters

- `fun` (*callable*)
  ``fun(x) -> (g, jac)``.

- `x` (*numpy.ndarray*)
  Candidate solution, for example ``result.x`` from `pymrm.newton`.

- `tol` (*float, optional*)
  Acceptance threshold on the backward error.

### Returns

- `dict`
  ``ok`` (bool), ``backward_error`` and ``max_abs_residual``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/checks.py#L207-L239)

```python
def residual_check(fun, x, tol=1e-8):
    """Judge a solution by its componentwise backward error.

    An absolute threshold on the residual depends on the units and scaling of
    the equations. The backward error ``max_i |g_i| / (|J| |x| + |J x - g|)_i``
    is scale-free: it measures the relative change in the (linearised) equation
    coefficients that would make ``x`` exact.

    Parameters
    ----------
    fun : callable
        ``fun(x) -> (g, jac)``.
    x : numpy.ndarray
        Candidate solution, for example ``result.x`` from :func:`pymrm.newton`.
    tol : float, optional
        Acceptance threshold on the backward error.

    Returns
    -------
    dict
        ``ok`` (bool), ``backward_error`` and ``max_abs_residual``.
    """
    x = np.asarray(x, dtype=float)
    g, jac = fun(x.copy())
    g = _as_dense_vector(g)
    x_flat = x.ravel()
    jac = sparse.csr_array(jac) if sparse.issparse(jac) else np.asarray(jac, dtype=float)
    abs_jac = abs(jac)
    denominator = abs_jac @ np.abs(x_flat) + np.abs(jac @ x_flat - g)
    denominator = np.where(denominator > 0.0, denominator, np.finfo(float).tiny)
    backward_error = float(np.max(np.abs(g) / denominator))
    return {"ok": bool(backward_error <= tol), "backward_error": backward_error,
            "max_abs_residual": float(np.max(np.abs(g)))}
```
