# `pymrm.solve`

[Back to modules overview](../api)

Nonlinear-solver utilities used by `pymrm`.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/solve.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`clip_approach`](../symbols/pymrm.solve.clip_approach) | function | Project values onto bounds, optionally with a relaxed approach rule. |
| [`newton`](../symbols/pymrm.solve.newton) | function | Solve ``function(x) = 0`` with Newton iterations. |

## `clip_approach(values, dummy, lower_bounds = 0, upper_bounds = None, factor = 0)`

[Open dedicated reference page](../symbols/pymrm.solve.clip_approach)

Project values onto bounds, optionally with a relaxed approach rule.

### Parameters

- `values` (*numpy.ndarray*)
  Values to modify in place.

- `dummy` (*Any*)
  Placeholder argument kept for API compatibility.

- `lower_bounds, upper_bounds` (*float or numpy.ndarray, optional*)
  Lower and upper bounds. Scalars and broadcastable arrays are supported.

- `factor` (*float, optional*)
  Relaxation factor for out-of-bound entries. ``0`` applies strict clipping.
  Non-zero values apply a linear approach update toward the violated bound.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/solve.py#L159-L190)

## `newton(function, initial_guess, args = (), tol = 1.49012e-08, maxfev = 100, solver = None, lin_solver_kwargs = None, callback = None, rtol = 0.0)`

[Open dedicated reference page](../symbols/pymrm.solve.newton)

Solve ``function(x) = 0`` with Newton iterations.

### Parameters

- `function` (*callable*)
  Callable with signature ``function(x, *args) -> (residual, jacobian)``.

- `initial_guess` (*numpy.ndarray*)
  Starting point of the iterations.

- `args` (*tuple, optional*)
  Extra positional arguments passed to ``function``.

- `tol` (*float or numpy.ndarray, optional*)
  Absolute stopping tolerance on the Newton update. With the default
  ``rtol=0`` and a scalar ``tol`` the iteration stops when the infinity
  norm of the update is below ``tol``. This is an ABSOLUTE criterion: for
  unknowns much smaller than ``tol`` (trace concentrations, for example)
  it can stop after one step with a wrong answer. Scale the unknowns to order
  one, or use ``tol=0`` with ``rtol``. An array must broadcast to the
  unknowns.

- `maxfev` (*int, optional*)
  Maximum number of Newton iterations.

- `solver` (*{'spsolve', 'cg', 'bicgstab', 'splu'} or callable, optional*)
  Linear solver used for each Newton step. If ``None``, the routine picks
  ``'spsolve'`` for smaller systems and ``'bicgstab'`` for larger systems.
  When ``'splu'`` is selected, the Jacobian returned by ``function`` is
  expected to be an already-decomposed ``SuperLU`` object (as returned by
  `scipy.sparse.linalg.splu`), and the solve step calls its
  ``.solve()`` method directly.
  A callable solver must accept ``(jac_matrix, rhs, **kwargs)`` and return
  the solution vector.

- `lin_solver_kwargs` (*dict, optional*)
  Keyword arguments forwarded to the selected linear solver.

- `callback` (*callable, optional*)
  Optional hook called as ``callback(x, residual)`` after each iteration.

- `rtol` (*float, optional*)
  Relative stopping tolerance. When ``rtol > 0`` or ``tol`` is an array,
  the iteration stops when every component satisfies
  ``abs(update) <= tol + rtol * abs(x)``. ``tol=0, rtol=1e-8`` gives a
  purely relative criterion.

### Returns

- `scipy.optimize.OptimizeResult`
  Result object with fields ``x``, ``success``, ``nit``, ``fun``,
  ``message`` and ``step_norm`` (infinity norm of the last update).
  ``fun`` is the residual evaluated at the iterate BEFORE the last update,
  not at ``x``; evaluate ``function(x)`` to check the final residual.

### Raises

- `ValueError`
  If ``solver`` is not one of the supported names and is not callable.

- `RuntimeError`
  If an iterative linear solver fails to converge.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/solve.py#L10-L156)
