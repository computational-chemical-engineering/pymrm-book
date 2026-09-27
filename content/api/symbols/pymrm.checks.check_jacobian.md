# `pymrm.checks.check_jacobian`

[Back to module page](../modules/pymrm.checks) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`check_jacobian(fun, x, n_probe = 4, rtol = 0.0001, seed = 0, eps = None)`

## Summary

Compare the Jacobian returned by ``fun`` with central differences.

## Documentation

### Parameters

- `fun` (*callable*)
  ``fun(x) -> (g, jac)``, the residual and its Jacobian, as passed to
  `pymrm.newton`. ``jac`` must be a matrix (not a factorisation).

- `x` (*numpy.ndarray*)
  State at which to compare. Use a state away from the solution, where
  all terms are active.

- `n_probe` (*int, optional*)
  Number of random directions ``v`` for which ``jac @ v`` is compared with
  a central difference of ``g``.

- `rtol` (*float, optional*)
  Tolerance on the relative mismatch.

- `seed` (*int, optional*)
  Seed of the random directions (the check is deterministic).

- `eps` (*float, optional*)
  Relative finite-difference step; default ``cbrt(machine epsilon)``.
  Each component is perturbed in proportion to its own size.

### Returns

- `dict`
  ``ok`` (bool), ``max_rel_error`` over the probes, and, for at most 500
  unknowns, ``worst_entry`` ``(row, col, jac_value, fd_value)`` from a full
  column-by-column comparison.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/checks.py#L26-L95)

```python
def check_jacobian(fun, x, n_probe=4, rtol=1e-4, seed=0, eps=None):
    """Compare the Jacobian returned by ``fun`` with central differences.

    Parameters
    ----------
    fun : callable
        ``fun(x) -> (g, jac)``, the residual and its Jacobian, as passed to
        :func:`pymrm.newton`. ``jac`` must be a matrix (not a factorisation).
    x : numpy.ndarray
        State at which to compare. Use a state away from the solution, where
        all terms are active.
    n_probe : int, optional
        Number of random directions ``v`` for which ``jac @ v`` is compared with
        a central difference of ``g``.
    rtol : float, optional
        Tolerance on the relative mismatch.
    seed : int, optional
        Seed of the random directions (the check is deterministic).
    eps : float, optional
        Relative finite-difference step; default ``cbrt(machine epsilon)``.
        Each component is perturbed in proportion to its own size.

    Returns
    -------
    dict
        ``ok`` (bool), ``max_rel_error`` over the probes, and, for at most 500
        unknowns, ``worst_entry`` ``(row, col, jac_value, fd_value)`` from a full
        column-by-column comparison.
    """
    x = np.asarray(x, dtype=float)
    shape = x.shape
    x_flat = x.ravel()
    g0, jac = fun(x.copy())
    g0 = _as_dense_vector(g0)
    jac = sparse.csr_array(jac) if sparse.issparse(jac) else np.asarray(jac, dtype=float)
    step = eps if eps is not None else np.finfo(float).eps ** (1.0 / 3.0)
    # per-component scale, so small unknowns are not pushed across zero
    x_scale = np.maximum(np.abs(x_flat), np.sqrt(np.finfo(float).eps) * max(np.max(np.abs(x_flat)), 1.0))
    noise = np.finfo(float).eps * np.abs(g0) / step

    def g_at(xf):
        return _as_dense_vector(fun(xf.reshape(shape).copy())[0])

    def mismatch(direction):
        fd = (g_at(x_flat + step * direction) - g_at(x_flat - step * direction)) / (2.0 * step)
        jv = jac @ direction
        if not (np.all(np.isfinite(fd)) and np.all(np.isfinite(jv))):
            return np.inf
        scale = np.abs(jv) + np.abs(fd) + noise
        err = np.abs(jv - fd) / np.where(scale > 0.0, scale, 1.0)
        return float(np.max(err))

    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(n_probe):
        worst = max(worst, mismatch(rng.standard_normal(x_flat.size) * x_scale))
    result = {"ok": bool(worst <= rtol), "max_rel_error": float(worst), "worst_entry": None}

    if x_flat.size <= 500:
        dense = jac.toarray() if sparse.issparse(jac) else jac
        fd_full = np.empty_like(dense)
        for k in range(x_flat.size):
            e = np.zeros(x_flat.size)
            e[k] = step * x_scale[k]
            fd_full[:, k] = (g_at(x_flat + e) - g_at(x_flat - e)) / (2.0 * e[k])
        diff = np.abs(dense - fd_full)
        diff = np.where(np.isfinite(diff), diff, np.inf)
        row, col = np.unravel_index(np.argmax(diff), diff.shape)
        result["worst_entry"] = (int(row), int(col), float(dense[row, col]), float(fd_full[row, col]))
    return result
```
