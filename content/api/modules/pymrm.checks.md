# `pymrm.checks`

[Back to modules overview](../api)

Deterministic checks for pymrm models.

Small tools for the verification steps every model needs, so that they do not
have to be rewritten (and debugged) for each model:

* `check_jacobian` compares a Jacobian with finite differences;
* `observed_orders` runs a refinement study and reports observed orders;
* `find_roots` locates every sign change of a scalar function in a range;
* `residual_check` judges a converged solution by a scale-free backward
  error instead of an absolute residual threshold.

The module depends on numpy and scipy only.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/checks.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`check_jacobian`](../symbols/pymrm.checks.check_jacobian) | function | Compare the Jacobian returned by ``fun`` with central differences. |
| [`find_roots`](../symbols/pymrm.checks.find_roots) | function | Locate every sign change of ``f`` on ``[lo, hi]`` and refine each root. |
| [`observed_orders`](../symbols/pymrm.checks.observed_orders) | function | Run a refinement study and report observed orders of convergence. |
| [`residual_check`](../symbols/pymrm.checks.residual_check) | function | Judge a solution by its componentwise backward error. |

## `check_jacobian(fun, x, n_probe = 4, rtol = 0.0001, seed = 0, eps = None)`

[Open dedicated reference page](../symbols/pymrm.checks.check_jacobian)

Compare the Jacobian returned by ``fun`` with central differences.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/checks.py#L26-L95)

## `find_roots(f, lo, hi, n_scan = 64, log = False, xtol = 1e-12)`

[Open dedicated reference page](../symbols/pymrm.checks.find_roots)

Locate every sign change of ``f`` on ``[lo, hi]`` and refine each root.

### Parameters

- `f` (*callable*)
  Scalar function. It may raise, or return ``nan``, where the underlying
  model cannot be evaluated; such points are reported, never taken as a
  sign.

- `lo, hi` (*float*)
  Physically possible range.

- `n_scan` (*int, optional*)
  Number of scan points.

- `log` (*bool, optional*)
  Scan on a logarithmic grid (``lo`` and ``hi`` must be positive).

- `xtol` (*float, optional*)
  Absolute tolerance of each refined root (``brentq`` ``xtol``).

### Returns

- `dict`
  ``roots`` (sorted list), ``failed`` (scan points where ``f`` could not
  be evaluated) and ``message``. No sign change gives an empty list and
  says so; it does NOT widen the range.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/checks.py#L155-L204)

## `observed_orders(solve, ns, ratio = None)`

[Open dedicated reference page](../symbols/pymrm.checks.observed_orders)

Run a refinement study and report observed orders of convergence.

### Parameters

- `solve` (*callable*)
  ``solve(n) -> float or array``, the quantity of interest computed with
  resolution ``n`` (cells, or number of time steps). An array must have
  the same shape at every resolution (for example values at fixed
  positions).

- `ns` (*sequence[int]*)
  At least three resolutions with a constant refinement ratio, for example
  ``(50, 100, 200, 400)``.

- `ratio` (*float, optional*)
  Refinement ratio; default ``ns[1] / ns[0]``.

### Returns

- `dict`
  ``values`` per resolution, ``orders`` from each consecutive triple,
  ``extrapolated`` (Richardson estimate from the finest triple) and
  ``error_estimate`` of the finest value against it; ``nan`` when the
  finest order is not positive (the study is not converging).

### Notes

The order from values ``q1, q2, q3`` on successively finer grids is
``log(|q1 - q2| / |q2 - q3|) / log(ratio)``; it needs no exact solution. An
order far from the expected one means the study is not in the asymptotic
range, the refinement does not control the error that dominates, or there is
a bug. For a non-uniform grid, refine it in a nested way (see the pymrm
agent plugin's profiles.md).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/checks.py#L98-L152)

## `residual_check(fun, x, tol = 1e-08)`

[Open dedicated reference page](../symbols/pymrm.checks.residual_check)

Judge a solution by its componentwise backward error.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/checks.py#L207-L239)
