# `pymrm.solve`

[Back to modules overview](../api)

Nonlinear-solver utilities used by `pymrm`.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/solve.py)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/solve.py#L115-L146)

## `newton(function, initial_guess, args = (), tol = 1.49012e-08, maxfev = 100, solver = None, lin_solver_kwargs = None, callback = None)`

[Open dedicated reference page](../symbols/pymrm.solve.newton)

Solve ``function(x) = 0`` with Newton iterations.

### Parameters

- `function` (*callable*)
  Callable with signature ``function(x, *args) -> (residual, jacobian)``.

- `initial_guess` (*numpy.ndarray*)
  Starting point of the iterations.

- `args` (*tuple, optional*)
  Extra positional arguments passed to ``function``.

- `tol` (*float, optional*)
  Stopping tolerance on the infinity norm of the Newton update.

- `maxfev` (*int, optional*)
  Maximum number of Newton iterations.

- `solver` (*{'spsolve', 'cg', 'bicgstab'} or callable, optional*)
  Linear solver used for each Newton step. If ``None``, the routine picks
  ``'spsolve'`` for smaller systems and ``'bicgstab'`` for larger systems.
  A callable solver must accept ``(jac_matrix, rhs, **kwargs)`` and return
  the solution vector.

- `lin_solver_kwargs` (*dict, optional*)
  Keyword arguments forwarded to the selected linear solver.

- `callback` (*callable, optional*)
  Optional hook called as ``callback(x, residual)`` after each iteration.

### Returns

- `scipy.optimize.OptimizeResult`
  Result object with fields ``x``, ``success``, ``nit``, ``fun``, and
  ``message``.

### Raises

- `ValueError`
  If ``solver`` is not one of the supported names and is not callable.

- `RuntimeError`
  If an iterative linear solver fails to converge.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/solve.py#L9-L112)
