# `pymrm.solve`

[Back to modules overview](../api)

Nonlinear-solver utilities used by `pymrm`.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`KrylovBreakdown`](../symbols/pymrm.solve.KrylovBreakdown) | class | An iterative linear solver did not converge (status 6). |
| [`NewtonBreakdown`](../symbols/pymrm.solve.NewtonBreakdown) | class | Raised by `newton` when no Newton step can be formed. |
| [`clip_approach`](../symbols/pymrm.solve.clip_approach) | function | Project values onto bounds, optionally with a relaxed approach rule. |
| [`continuation`](../symbols/pymrm.solve.continuation) | function | Solve ``function(x, p) = 0`` along a sequence of parameter values. |
| [`newton`](../symbols/pymrm.solve.newton) | function | Solve ``function(x) = 0`` with a (damped) Newton iteration. |
| [`pseudo_transient`](../symbols/pymrm.solve.pseudo_transient) | function | Reach a steady state of ``function(x) = 0`` by implicit pseudo-time steps. |

## `KrylovBreakdown(message, result = None)`

[Open dedicated reference page](../symbols/pymrm.solve.KrylovBreakdown)

An iterative linear solver did not converge (status 6).

Also a ``RuntimeError``, as raised up to pymrm 2.5.0.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L56-L60)

## Members

### `__init__(message, result = None)`

Initialize self.  See help(type(self)) for accurate signature.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L51-L53)

### `__delattr__()`

Implement delattr(self, name).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__dir__()`

Default dir() implementation.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__eq__()`

Return self==value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__format__()`

Default object formatter.

Return str(self) if format_spec is empty. Raise TypeError otherwise.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__ge__()`

Return self>=value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__getattribute__()`

Return getattr(self, name).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__getstate__()`

Helper for pickle.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__gt__()`

Return self>value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__hash__()`

Return hash(self).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__le__()`

Return self<=value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__lt__()`

Return self<value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__ne__()`

Return self!=value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__new__()`

Create and return a new object.  See help(type) for accurate signature.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__reduce__()`

Helper for pickle.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__reduce_ex__()`

Helper for pickle.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__repr__()`

Return repr(self).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__setattr__()`

Implement setattr(self, name, value).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__setstate__()`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__sizeof__()`

Size of object in memory, in bytes.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__str__()`

Return str(self).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__subclasshook__()`

Abstract classes can override this to customize issubclass().

This is invoked early on by abc.ABCMeta.__subclasscheck__().
It should return True, False or NotImplemented.  If it returns
NotImplemented, the normal algorithm is used.  Otherwise, it
overrides the normal algorithm (and the outcome is cached).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `add_note()`

Exception.add_note(note) -- add a note to the exception

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `with_traceback()`

Exception.with_traceback(tb) -- set self.__traceback__ to tb and return self.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

## `NewtonBreakdown(message, result = None)`

[Open dedicated reference page](../symbols/pymrm.solve.NewtonBreakdown)

Raised by `newton` when no Newton step can be formed.

A singular Jacobian (status 5), a non-finite residual or Jacobian that no
damping can avoid (status 4) or a non-finite Newton step (status 6). It is
a ``LinAlgError`` and so a ``ValueError``, as the exceptions these cases
raised up to pymrm 2.5.0. ``result`` holds the
`scipy.optimize.OptimizeResult` with the status and the last
iterate ``x``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L40-L53)

## Members

### `__init__(message, result = None)`

Initialize self.  See help(type(self)) for accurate signature.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L51-L53)

### `__delattr__()`

Implement delattr(self, name).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__dir__()`

Default dir() implementation.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__eq__()`

Return self==value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__format__()`

Default object formatter.

Return str(self) if format_spec is empty. Raise TypeError otherwise.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__ge__()`

Return self>=value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__getattribute__()`

Return getattr(self, name).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__getstate__()`

Helper for pickle.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__gt__()`

Return self>value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__hash__()`

Return hash(self).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__le__()`

Return self<=value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__lt__()`

Return self<value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__ne__()`

Return self!=value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__new__()`

Create and return a new object.  See help(type) for accurate signature.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__reduce__()`

Helper for pickle.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__reduce_ex__()`

Helper for pickle.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__repr__()`

Return repr(self).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__setattr__()`

Implement setattr(self, name, value).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__setstate__()`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__sizeof__()`

Size of object in memory, in bytes.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__str__()`

Return str(self).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `__subclasshook__()`

Abstract classes can override this to customize issubclass().

This is invoked early on by abc.ABCMeta.__subclasscheck__().
It should return True, False or NotImplemented.  If it returns
NotImplemented, the normal algorithm is used.  Otherwise, it
overrides the normal algorithm (and the outcome is cached).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `add_note()`

Exception.add_note(note) -- add a note to the exception

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

### `with_traceback()`

Exception.with_traceback(tb) -- set self.__traceback__ to tb and return self.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L0-L0)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L1145-L1176)

## `continuation(function, initial_guess, params, *, max_halvings = 6, max_change = 0.2, newton_kwargs = None, verbose = 0)`

[Open dedicated reference page](../symbols/pymrm.solve.continuation)

Solve ``function(x, p) = 0`` along a sequence of parameter values.

Natural-parameter continuation: each point starts from a secant
extrapolation of the two previous solutions and is corrected with
`newton`. A failed correction halves the parameter step (at most
``max_halvings`` times per requested value). A correction that moves
``x`` by more than ``max_change`` times ``max |x|`` from the prediction
counts as failed: near a turning point (fold) the corrector otherwise
jumps silently to another solution branch. The march then stops and
reports where; the fold lies between the last parameter reached and the
next one. Following a branch around a fold needs arclength continuation,
which this function does not do.

### Parameters

- `function` (*callable*)
  ``function(x, p) -> (residual, jacobian)``.

- `initial_guess` (*numpy.ndarray*)
  Guess for the first parameter value.

- `params` (*sequence of float*)
  Parameter values, in the order to visit them.

- `max_halvings` (*int, optional*)
  Largest number of step halvings on the way to one parameter value.

- `max_change` (*float or None, optional*)
  Largest accepted relative distance between prediction and solution;
  ``None`` disables the branch-jump check.

- `newton_kwargs` (*dict, optional*)
  Options for `newton`.

- `verbose` (*int, optional*)
  ``1`` prints one line per accepted point.

### Returns

- `scipy.optimize.OptimizeResult`
  ``success`` (every value reached), ``message``, ``params`` (the values
  reached), ``xs`` (their solutions), ``results`` (their `newton`
  results), ``last_param`` (the last parameter at which a solution was
  found, possibly an intermediate one) and ``x`` (that solution).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L1046-L1142)

## `newton(function, initial_guess, args = (), tol = 1.49012e-08, maxfev = 100, solver = None, lin_solver_kwargs = None, callback = None, rtol = 0.0, *, damping = 'auto', bounds = None, tau = 0.99, scale = None, refresh = None, backward_tol = 1e-08, stagnation = False, row_scaling = False, recoverable = (FloatingPointError, OverflowError, ZeroDivisionError), verbose = 0)`

[Open dedicated reference page](../symbols/pymrm.solve.newton)

Solve ``function(x) = 0`` with a (damped) Newton iteration.

Every iteration solves ``J dx = g`` with a direct sparse LU factorisation
and updates ``x <- x - lam dx``. With the default options the step length
``lam`` is 1 (plain Newton) unless the full step gives a non-finite
residual, and convergence requires both a small step (``tol``) and a small
backward error (``backward_tol``). For hard problems, ``damping``,
``bounds`` and ``scale`` make the iteration robust far from the solution;
see the Notes.

### Parameters

- `function` (*callable*)
  ``function(x, *args) -> (residual, jacobian)``. ``x`` has the shape of
  ``initial_guess``; the residual is flattened internally. The Jacobian
  is a scipy sparse matrix or array, a dense array, or, with
  ``solver='splu'``, an already factorised ``SuperLU`` object.

- `initial_guess` (*numpy.ndarray*)
  Starting point; it is copied, not modified.

- `args` (*tuple, optional*)
  Extra positional arguments passed to ``function``.

- `tol` (*float or numpy.ndarray, optional*)
  Stopping tolerance on the Newton step. With the default ``rtol=0`` and
  a scalar ``tol`` the step test is ``max |dx| < tol``. This is an
  ABSOLUTE criterion: for unknowns much smaller than ``tol`` (trace
  concentrations) it can stop after one step with a wrong answer. Scale
  the unknowns to order one (``scale``), use ``tol=0`` with ``rtol``, or
  set ``backward_tol``. An array must broadcast to the unknowns. With
  ``scale`` the test applies to the scaled step ``dx / scale``.

- `maxfev` (*int, optional*)
  Maximum number of Newton iterations (Jacobian factorisations), not of
  function evaluations; ``nfev`` in the result counts those.

- `solver` (*None, str, callable or object, optional*)
  Linear solver for ``J dx = g``.

  * ``None``, ``'spsolve'`` or ``'lu'``: direct LU at every size,
    ``scipy.sparse.linalg.splu`` (COLAMD ordering) for sparse Jacobians
    and ``scipy.linalg.lu_factor`` for dense ones. The factorisation is
    reused for the damping test. ``lin_solver_kwargs`` go to ``splu``.
  * ``'cg'``, ``'bicgstab'``: ILU-preconditioned Krylov solvers, only on
    request; ``lin_solver_kwargs`` go to the Krylov solver.
  * ``'splu'``: ``function`` returns an already factorised ``SuperLU``
    object instead of a matrix; its ``.solve()`` is used.
  * an object with a ``factorize(jac)`` method returning an object with
    ``.solve(rhs)``: a user factorisation (for example a Schur
    complement) that takes part in the damping test.
  * a callable ``solver(jac, rhs, **lin_solver_kwargs) -> dx``.

- `lin_solver_kwargs` (*dict, optional*)
  Keyword arguments forwarded to the linear solver.

- `callback` (*callable, optional*)
  ``callback(x, residual)`` after each accepted step, with ``residual``
  the residual before the step. It may modify ``x`` in place (for
  example `clip_approach`); the change is kept.

- `rtol` (*float, optional*)
  Relative stopping tolerance. When ``rtol > 0`` or ``tol`` is an array,
  the step test is ``abs(dx) <= tol + rtol * abs(x)`` for every
  component. ``tol=0, rtol=1e-8`` gives a purely relative criterion.

- `damping` (*{'auto', 'none', 'guarded', 'monotone', 'armijo'}, optional*)
  Globalisation of the step.

  * ``'none'``: full Newton steps (shortened only by ``bounds``).
  * ``'guarded'``: full steps, unless the residual at the full step is
    not finite or its evaluation raises one of ``recoverable``; only
    then is the step shortened by the monotone search. Where plain
    Newton works it takes exactly the same steps.
  * ``'monotone'``: Deuflhard's natural monotonicity test. A step length
    ``lam`` is accepted when the simplified Newton correction at the
    trial point, ``J(x)^{-1} g(x - lam dx)``, is smaller than
    ``(1 - lam/4)`` times ``dx`` (root mean square, scaled by
    ``scale``); otherwise ``lam`` is reduced. Independent of how the
    residual rows are scaled; costs one back substitution per trial.
    When no step length above 1e-4 passes (0.2 near the solution), the
    full step is taken if its residual is finite: the test cannot see
    past a turning point, which full steps sometimes jump.
  * ``'armijo'``: backtracking until the row-equilibrated residual norm
    decreases by the Armijo condition, with the same fallback. Use it
    when the simplified correction is unavailable or meaningless.
  * ``'auto'`` (default): ``'guarded'``, but ``'none'`` whenever a
    ``callback`` or a callable ``solver`` is given, since those may
    change the step after it is taken.

  Measured on 84 Arrhenius (Weisz-Hicks) pellets from three starts:
  ``'none'`` 60 converged, ``'guarded'`` 62 at the same cost,
  ``'monotone'`` 69 at about twice the function evaluations. On
  half-order kinetics with a dead zone ``'monotone'`` with regularised
  kinetics converged in every case, plain Newton in a third.

- `bounds` (*float, array, tuple, or scipy.optimize.Bounds, optional*)
  ``(lower, upper)``; each side ``None``, a scalar, or an array that
  broadcasts against the shape of ``initial_guess`` (shape ``(nc,)``
  gives one bound per field, ``(nz, 1)`` one per cell). Use ``-np.inf``
  or ``np.inf`` for unbounded components. A single scalar or array means
  a lower bound. No step removes more than ``tau`` of the distance of a
  component to its bound (with a floor of 0.5 on ``lam``, below which
  the components are projected individually). A component may sit on
  its bound; an initial guess outside is projected, with a warning.
  Use bounds where the residual is undefined (``T > 0``, arguments of
  ``log`` or ``sqrt``), not to enforce physical positivity: see Notes.

- `tau` (*float, optional*)
  Fraction-to-the-boundary parameter of ``bounds``.

- `scale` (*float or numpy.ndarray, optional*)
  Typical magnitude of the unknowns, broadcast against
  ``initial_guess``. The step test, the damping test and the stagnation
  rule are applied to ``x / scale``.

- `refresh` (*callable, optional*)
  ``refresh(x)`` after every accepted step, for quantities the caller
  updates outside the Jacobian (lagged velocities, properties). The
  residual is re-evaluated afterwards. The damping test is then
  approximate, and the stagnation rule is off.

- `backward_tol` (*float or None, optional*)
  If not None (default ``1e-8``), the step test is necessary but not
  sufficient (unless the Jacobian is not a matrix, so that the backward
  error cannot be formed): the backward error of the iterate the step is
  taken from must also be below ``backward_tol``, else the iteration
  continues. The final Newton step then only improves it, and no
  evaluation is spent beyond those of plain Newton. The backward error is
  ``max_i |g_i| / (|J| (|x| + x_ref) + |J x - g|)_i``, the relative
  change of the equation coefficients that would make ``x`` exact, with
  ``x_ref`` the magnitude of each unknown's field: ``scale`` if given,
  else the largest ``|x|`` of that field (fields along the last axis; a
  one-dimensional state is one field). Components far below their
  field's magnitude, such as a reaction dead zone, are thus judged
  against the field, while a field that is small everywhere (a trace
  species) is judged against itself, down to ``1e-6`` of the largest
  unknown. It is always reported in the result. For a flat state that
  mixes units, pass ``scale``. ``None`` restores the plain step test.

- `stagnation` (*bool, optional*)
  Stop at the stagnation floor: when the step test cannot be met because
  round-off, or switching terms such as ``max(c, 0)`` and upwinding, keep
  the steps from shrinking, a full step within 100 tolerances that is no
  smaller than the smallest of the five before it ends the iteration with
  success, provided ``backward_tol`` passes; otherwise the iteration
  continues. A converging iteration, however slowly, makes a new smallest
  step every time and is never stopped. Off by default: code written for
  the old iteration may rely on a ``tol`` below the floor failing.

- `row_scaling` (*bool, optional*)
  Divide each row of the Jacobian by its largest entry before the direct
  LU factorisation. Improves pivoting when rows have different units.
  Off by default: it changes the pivot order and with it the round-off,
  and continuations that pass close to a turning point with a
  tolerance near round-off then end on a different branch (measured on
  a gallery page).

- `recoverable` (*tuple of exception types, optional*)
  Exceptions that mark a damped trial point as unusable: the step is
  shortened. Non-finite residuals are treated the same way. Exceptions
  at the initial guess, and in undamped iterations, propagate.

- `verbose` (*int, optional*)
  ``1`` prints one line per iteration.

### Returns

- `scipy.optimize.OptimizeResult`
  ``x`` (shape of ``initial_guess``), ``success``, ``status``,
  ``message``, ``nit`` (Newton iterations), ``nfev`` (function
  evaluations), ``nfact`` (factorisations), ``fun`` (the residual of
  the last evaluated iterate, as returned by ``function``: for a
  converged solve the iterate before the final step, which ``x`` only
  improves; evaluate ``function(x)`` for the residual at ``x``),
  ``step_norm`` (infinity norm of the last Newton step),
  ``backward_error`` (of the same iterate as ``fun``; ``nan`` when the
  Jacobian is not a matrix), and ``history``, a list with per
  iteration ``step_norm``, ``damping``, ``theta`` (monotonicity ratio)
  and ``clipped`` (components held by a bound).

  ``status``: 0 converged; 1 converged to the stagnation floor;
  2 ``maxfev`` reached; 3 damping fell below its minimum; 7 step test
  met but ``backward_error > backward_tol``; 8 stopped on a bound (the
  bound is likely cutting off the solution). Statuses 4 (non-finite
  residual or Jacobian that no damping avoids), 5 (singular Jacobian)
  and 6 (non-finite Newton step, or an iterative linear solver that did
  not converge) are raised as `NewtonBreakdown`, whose ``result``
  holds this object.

### Raises

- `ValueError`
  If ``solver``, ``damping`` or ``scale`` is not supported.

- `NewtonBreakdown`
  When no Newton step can be formed (statuses 4 to 6). It is a
  ``numpy.linalg.LinAlgError`` and so a ``ValueError``, as the
  exceptions these cases raised up to 2.5.0; `KrylovBreakdown`
  (an iterative solver failed) is also a ``RuntimeError``.

### Notes

**When plain Newton fails.** Far from the solution a full step can leave
the region where the residual is meaningful (a negative concentration or
temperature), and the iteration ends in a non-finite residual or
diverges. ``damping='guarded'`` handles the non-finite case at no cost
elsewhere. Use ``damping='monotone'`` when full steps overshoot without
producing non-finite values; add ``scale`` when unknowns of
different units are mixed (it makes the step and damping tests weigh
them equally), and ``bounds`` only for unknowns that the residual cannot
accept beyond a limit. Where a solution depends on a parameter, warm
starts along that parameter (continuation) remain the most reliable
route; damping does not choose between multiple solutions.

**Kinetics near zero concentration.** A hard lower bound at zero often
hurts convergence: the discrete solution may itself be slightly negative
near steep fronts, and ``max(c, 0)`` in a rate makes its derivative zero
below zero, so the Jacobian loses the term that pulls ``c`` back. Prefer
rates that are smooth through zero and first order near it, for example
``k c (c**2 + eps**2)**((n - 1)/2)`` instead of ``k c**n`` with ``n < 1``,
or ``c / (1 + K abs(c))`` for Langmuir-Hinshelwood forms, with ``eps`` a
small fraction of a reference concentration (check that results do not
change when it is reduced tenfold). A guard bound below zero, such as
``bounds=(-1e-3 * c_ref, None)``, then only stops wild overshoots.

**Convergence verdict.** The step test is absolute. A trace unknown much
smaller than ``tol`` passes it immediately; the default
``backward_tol=1e-8`` then keeps the iteration going until the residual
is also small relative to the equations, without changing the meaning of
``tol``. `pymrm.checks.residual_check` gives a stricter, purely
componentwise verdict after the fact.

**Changes in 3.0.0.** Before, ``newton`` took plain full steps even
into a non-finite residual, stopped on the step test alone, and switched
to ILU-BiCGSTAB above 50 000 unknowns. Pass ``damping="none",
backward_tol=None`` for the old iteration; it then
takes the same steps, evaluations and results as before. A singular
Jacobian, a non-finite residual or step, or an iterative linear solver
that does not converge still raise, now as `NewtonBreakdown`
with the result attached.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L337-L907)

## `pseudo_transient(function, initial_guess, mass = 1.0, dt = 0.001, args = (), *, dt_max = np.inf, max_steps = 200, growth = 10.0, steady_ratio = 0.1, steady_every = 10, newton_kwargs = None, steady_kwargs = None, verbose = 0)`

[Open dedicated reference page](../symbols/pymrm.solve.pseudo_transient)

Reach a steady state of ``function(x) = 0`` by implicit pseudo-time steps.

When Newton from the initial guess fails (ignition, extinction, a guess
far from any solution), march ``mass dx/dt = -function(x)`` with implicit
Euler steps instead: each step solves
``function(x) + mass (x - x_old) / dt = 0`` with `newton`, which is
well conditioned for small ``dt``. After a step whose Newton solve took
at most 3 iterations ``dt`` doubles, or grows by the residual reduction
``||g_old|| / ||g||`` when that is larger (switched evolution relaxation;
at most ``growth`` per step and at most ``dt_max``); after a harder step it
is kept, and a failed step is retried with ``dt / 4``. The residual may
rise for a while, as it does through an ignition.

Measured on the Weisz-Hicks pellets where ``newton(...,
damping="guarded")`` fails: the march reached the steady state in 18 of
22, mostly within 20 steps. The four it did not reach (a steep reaction
front crawling at tiny ``dt``) were solved by ``damping="monotone"``;
try both. A steady Newton solve from the current state is
tried every ``steady_every`` steps and whenever the residual norm has
dropped by ``steady_ratio`` since the last attempt; it ends the march when
it converges.

### Parameters

- `function` (*callable*)
  ``function(x, *args) -> (residual, jacobian)``, as for `newton`,
  with a matrix Jacobian.

- `initial_guess` (*numpy.ndarray*)
  Starting state.

- `mass` (*float, numpy.ndarray or sparse matrix, optional*)
  Accumulation term: a scalar or an array broadcast against the state
  (a diagonal), or a matrix. It sets the relative speed of the fields in
  pseudo-time and must have the units of the residual per unit of the
  state; 1 suits residuals scaled like the state.

- `dt` (*float, optional*)
  First pseudo-time step.

- `args` (*tuple, optional*)
  Extra arguments of ``function``.

- `dt_max` (*float, optional*)
  Largest pseudo-time step.

- `max_steps` (*int, optional*)
  Largest number of accepted pseudo-time steps.

- `growth` (*float, optional*)
  Largest factor by which ``dt`` grows per step.

- `steady_ratio` (*float, optional*)
  Try the steady solve each time the residual norm has dropped by this
  factor.

- `steady_every` (*int, optional*)
  Try the steady solve at least every so many steps.

- `newton_kwargs` (*dict, optional*)
  Options for the Newton solve of each step (default ``maxfev=10``,
  ``damping="guarded"``).

- `steady_kwargs` (*dict, optional*)
  Options for the steady Newton solves (default ``maxfev=30``,
  ``damping="guarded"``).

- `verbose` (*int, optional*)
  ``1`` prints one line per step.

### Returns

- `scipy.optimize.OptimizeResult`
  ``x``, ``success``, ``message``, ``nsteps``, ``history`` (``dt``,
  residual norm and Newton iterations per step) and ``steady`` (the
  last steady `newton` result).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L926-L1043)
