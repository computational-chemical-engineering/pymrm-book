# `pymrm.solve.newton`

```python
newton(function, initial_guess, args = (), tol = 1.49012e-08, maxfev = 100, solver = None, lin_solver_kwargs = None, callback = None)
```

Solve ``function(x) = 0`` with Newton iterations.

**Parameters**

- **function** : `callable` — Callable with signature ``function(x, *args) -> (residual, jacobian)``.
- **initial_guess** : `numpy.ndarray` — Starting point of the iterations.
- **args** : `tuple` — Extra positional arguments passed to ``function``.
- **tol** : `float` — Stopping tolerance on the infinity norm of the Newton update.
- **maxfev** : `int` — Maximum number of Newton iterations.
- **solver** : `(spsolve, cg, bicgstab)` — Linear solver used for each Newton step. If ``None``, the routine picks
``'spsolve'`` for smaller systems and ``'bicgstab'`` for larger systems.
A callable solver must accept ``(jac_matrix, rhs, **kwargs)`` and return
the solution vector.
- **lin_solver_kwargs** : `dict` — Keyword arguments forwarded to the selected linear solver.
- **callback** : `callable` — Optional hook called as ``callback(x, residual)`` after each iteration.

**Returns**

- `scipy.optimize.OptimizeResult` — Result object with fields ``x``, ``success``, ``nit``, ``fun``, and
``message``.

**Raises**

- **ValueError** — If ``solver`` is not one of the supported names and is not callable.
- **RuntimeError** — If an iterative linear solver fails to converge.
