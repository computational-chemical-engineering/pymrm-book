# `pymrm.solve.newton`

[Back to module page](../modules/pymrm.solve) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`newton(function, initial_guess, args = (), tol = 1.49012e-08, maxfev = 100, solver = None, lin_solver_kwargs = None, callback = None, rtol = 0.0, *, damping = 'auto', bounds = None, tau = 0.99, scale = None, refresh = None, backward_tol = 1e-08, stagnation = False, row_scaling = False, recoverable = (FloatingPointError, OverflowError, ZeroDivisionError), verbose = 0)`

## Summary

Solve ``function(x) = 0`` with a (damped) Newton iteration.

## Documentation

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
  a lower bound. A full step that crosses a bound is shortened so that
  it removes at most ``tau`` of the distance of that component to its
  bound (with a floor of 0.5 on ``lam``, below which the crossing
  components are held individually). A full step that lands inside the
  bounds is taken, however close to a bound, so a solution near a bound
  still converges quadratically. A component may sit on its bound; an
  initial guess outside is projected, with a warning. Use bounds where
  the residual is undefined (``T > 0``, arguments of ``log`` or
  ``sqrt``), not to enforce physical positivity: see Notes. Where the
  residual is singular at the bound (``log``), prefer
  ``damping="monotone"``: a step may land very close to the bound.

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
  the steps from shrinking, a Newton step within 100 tolerances that is
  no smaller than the smallest of the five before it ends the iteration
  with success, provided ``backward_tol`` passes; otherwise the iteration
  continues. Steps the damping shortened count too: at the floor the
  damping test fails on round-off. A converging iteration, however slowly, makes a new smallest
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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/solve.py#L356-L934)

```python
def newton(
    function,
    initial_guess,
    args=(),
    tol=1.49012e-08,
    maxfev=100,
    solver=None,
    lin_solver_kwargs=None,
    callback=None,
    rtol=0.0,
    *,
    damping="auto",
    bounds=None,
    tau=0.99,
    scale=None,
    refresh=None,
    backward_tol=1e-8,
    stagnation=False,
    row_scaling=False,
    recoverable=(FloatingPointError, OverflowError, ZeroDivisionError),
    verbose=0,
):
    """Solve ``function(x) = 0`` with a (damped) Newton iteration.

    Every iteration solves ``J dx = g`` with a direct sparse LU factorisation
    and updates ``x <- x - lam dx``. With the default options the step length
    ``lam`` is 1 (plain Newton) unless the full step gives a non-finite
    residual, and convergence requires both a small step (``tol``) and a small
    backward error (``backward_tol``). For hard problems, ``damping``,
    ``bounds`` and ``scale`` make the iteration robust far from the solution;
    see the Notes.

    Parameters
    ----------
    function : callable
        ``function(x, *args) -> (residual, jacobian)``. ``x`` has the shape of
        ``initial_guess``; the residual is flattened internally. The Jacobian
        is a scipy sparse matrix or array, a dense array, or, with
        ``solver='splu'``, an already factorised ``SuperLU`` object.
    initial_guess : numpy.ndarray
        Starting point; it is copied, not modified.
    args : tuple, optional
        Extra positional arguments passed to ``function``.
    tol : float or numpy.ndarray, optional
        Stopping tolerance on the Newton step. With the default ``rtol=0`` and
        a scalar ``tol`` the step test is ``max |dx| < tol``. This is an
        ABSOLUTE criterion: for unknowns much smaller than ``tol`` (trace
        concentrations) it can stop after one step with a wrong answer. Scale
        the unknowns to order one (``scale``), use ``tol=0`` with ``rtol``, or
        set ``backward_tol``. An array must broadcast to the unknowns. With
        ``scale`` the test applies to the scaled step ``dx / scale``.
    maxfev : int, optional
        Maximum number of Newton iterations (Jacobian factorisations), not of
        function evaluations; ``nfev`` in the result counts those.
    solver : None, str, callable or object, optional
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
    lin_solver_kwargs : dict, optional
        Keyword arguments forwarded to the linear solver.
    callback : callable, optional
        ``callback(x, residual)`` after each accepted step, with ``residual``
        the residual before the step. It may modify ``x`` in place (for
        example :func:`clip_approach`); the change is kept.
    rtol : float, optional
        Relative stopping tolerance. When ``rtol > 0`` or ``tol`` is an array,
        the step test is ``abs(dx) <= tol + rtol * abs(x)`` for every
        component. ``tol=0, rtol=1e-8`` gives a purely relative criterion.
    damping : {'auto', 'none', 'guarded', 'monotone', 'armijo'}, optional
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
    bounds : float, array, tuple, or scipy.optimize.Bounds, optional
        ``(lower, upper)``; each side ``None``, a scalar, or an array that
        broadcasts against the shape of ``initial_guess`` (shape ``(nc,)``
        gives one bound per field, ``(nz, 1)`` one per cell). Use ``-np.inf``
        or ``np.inf`` for unbounded components. A single scalar or array means
        a lower bound. A full step that crosses a bound is shortened so that
        it removes at most ``tau`` of the distance of that component to its
        bound (with a floor of 0.5 on ``lam``, below which the crossing
        components are held individually). A full step that lands inside the
        bounds is taken, however close to a bound, so a solution near a bound
        still converges quadratically. A component may sit on its bound; an
        initial guess outside is projected, with a warning. Use bounds where
        the residual is undefined (``T > 0``, arguments of ``log`` or
        ``sqrt``), not to enforce physical positivity: see Notes. Where the
        residual is singular at the bound (``log``), prefer
        ``damping="monotone"``: a step may land very close to the bound.
    tau : float, optional
        Fraction-to-the-boundary parameter of ``bounds``.
    scale : float or numpy.ndarray, optional
        Typical magnitude of the unknowns, broadcast against
        ``initial_guess``. The step test, the damping test and the stagnation
        rule are applied to ``x / scale``.
    refresh : callable, optional
        ``refresh(x)`` after every accepted step, for quantities the caller
        updates outside the Jacobian (lagged velocities, properties). The
        residual is re-evaluated afterwards. The damping test is then
        approximate, and the stagnation rule is off.
    backward_tol : float or None, optional
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
    stagnation : bool, optional
        Stop at the stagnation floor: when the step test cannot be met because
        round-off, or switching terms such as ``max(c, 0)`` and upwinding, keep
        the steps from shrinking, a Newton step within 100 tolerances that is
        no smaller than the smallest of the five before it ends the iteration
        with success, provided ``backward_tol`` passes; otherwise the iteration
        continues. Steps the damping shortened count too: at the floor the
        damping test fails on round-off. A converging iteration, however slowly, makes a new smallest
        step every time and is never stopped. Off by default: code written for
        the old iteration may rely on a ``tol`` below the floor failing.
    row_scaling : bool, optional
        Divide each row of the Jacobian by its largest entry before the direct
        LU factorisation. Improves pivoting when rows have different units.
        Off by default: it changes the pivot order and with it the round-off,
        and continuations that pass close to a turning point with a
        tolerance near round-off then end on a different branch (measured on
        a gallery page).
    recoverable : tuple of exception types, optional
        Exceptions that mark a damped trial point as unusable: the step is
        shortened. Non-finite residuals are treated the same way. Exceptions
        at the initial guess, and in undamped iterations, propagate.
    verbose : int, optional
        ``1`` prints one line per iteration.

    Returns
    -------
    scipy.optimize.OptimizeResult
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
        not converge) are raised as :class:`NewtonBreakdown`, whose ``result``
        holds this object.

    Raises
    ------
    ValueError
        If ``solver``, ``damping`` or ``scale`` is not supported.
    NewtonBreakdown
        When no Newton step can be formed (statuses 4 to 6). It is a
        ``numpy.linalg.LinAlgError`` and so a ``ValueError``, as the
        exceptions these cases raised up to 2.5.0; :class:`KrylovBreakdown`
        (an iterative solver failed) is also a ``RuntimeError``.

    Notes
    -----
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
    ``tol``. :func:`pymrm.checks.residual_check` gives a stricter, purely
    componentwise verdict after the fact.

    **Changes in 3.0.0.** Before, ``newton`` took plain full steps even
    into a non-finite residual, stopped on the step test alone, and switched
    to ILU-BiCGSTAB above 50 000 unknowns. Pass ``damping="none",
    backward_tol=None`` for the old iteration; it then
    takes the same steps, evaluations and results as before. A singular
    Jacobian, a non-finite residual or step, or an iterative linear solver
    that does not converge still raise, now as :class:`NewtonBreakdown`
    with the result attached.
    """
    x = np.array(initial_guess, dtype=float, order="C")
    shape = x.shape
    n = x.size
    x_flat = x.reshape(-1)  # view: updates of x_flat update x
    with np.errstate(invalid="ignore"):
        x0_size = float(np.nanmax(np.abs(x_flat))) if n and np.any(np.isfinite(x_flat)) else 0.0

    if lin_solver_kwargs is None:
        lin_solver_kwargs = {}
    lin = _LinearSolver(solver, lin_solver_kwargs, row_scaling)

    if damping == "auto":
        user_hooks = callback is not None or lin.kind == "callable"
        mode = "none" if user_hooks else _AUTO_DAMPING
    elif damping in ("none", "guarded", "monotone", "armijo"):
        mode = damping
    else:
        raise ValueError(f"Unsupported damping {damping!r}.")
    lin.legacy = mode == "none" and not row_scaling
    legacy_exact = mode == "none" and backward_tol is None

    d_user = None if scale is None else \
        np.array(np.broadcast_to(np.asarray(scale, dtype=float), shape)).ravel()
    if d_user is not None and not (np.all(np.isfinite(d_user)) and np.all(d_user > 0.0)):
        raise ValueError("scale must be finite and positive for every unknown.")
    d = np.ones(n) if d_user is None else d_user
    relative = rtol > 0 or not np.isscalar(tol)
    tol_vec = np.array(np.broadcast_to(np.asarray(tol, dtype=float), shape)).ravel() \
        if relative else None
    bnd = _Bounds(*_parse_bounds(bounds, shape), tau)
    if bnd.active:
        bnd.enforce_initial(x_flat)
    use_stagnation = stagnation and refresh is None

    nfev = 0
    nfact = 0
    history = []
    state = {"last": False, "ev": None, "step": float("nan"), "bad": None}

    def evaluate(xv, guard):
        """Residual (flat) and Jacobian at ``xv``; None if unusable and guarded."""
        nonlocal nfev
        nfev += 1
        if guard:
            try:
                g_raw, jac = function(xv, *args)
            except recoverable:
                return None
            except Exception as exc:
                if state["last"]:
                    # The old iteration never evaluated here: report, do not raise.
                    raise _LastEvaluationFailed(f"{type(exc).__name__}: {exc}") from exc
                raise
        else:
            g_raw, jac = function(xv, *args)
        g_raw = g_raw.toarray() if sparse.issparse(g_raw) else np.array(g_raw, dtype=float)
        g_flat = g_raw.reshape(-1)
        if sparse.issparse(jac) and jac.format not in ("csr", "csc", "coo", "bsr", "dia"):
            jac = jac.tocsc()      # lil, dok: no .data array of the stored values
        finite = np.all(np.isfinite(g_flat))
        if finite and _is_matrix(jac):
            data = jac.data if sparse.issparse(jac) else jac
            finite = np.all(np.isfinite(data))
        if not finite:
            state["bad"] = g_raw
            return None
        return g_raw, g_flat, jac

    def backward_error(g_flat, jac):
        if not _is_matrix(jac):
            return float("nan")
        return _backward_error(g_flat, jac, x_flat,
                               _field_reference(x_flat, shape, d_user, x0_size))

    def finish(status, success, ev, step_norm, be, extra="", krylov=False):
        if ev is None:
            g_raw = state["bad"] if status == 4 else None
        else:
            g_raw = ev[0]
        message = _MESSAGES[status] + (f": {extra}" if extra else "")
        result = OptimizeResult(x=x, success=bool(success), status=status, message=message,
                                nit=len(history), nfev=nfev, nfact=nfact, fun=g_raw,
                                step_norm=step_norm, backward_error=be, history=history)
        if status in (4, 5, 6):
            # No usable Newton step: raise, as these cases did up to 2.5.0
            # (callers catch ValueError, LinAlgError or RuntimeError).
            raise (KrylovBreakdown if krylov else NewtonBreakdown)(message, result)
        return result

    ev = evaluate(x, guard=False)
    if ev is None:
        return finish(4, False, None, float("nan"), float("nan"), "at the initial guess")

    def iterate():
        nonlocal nfact, ev
        lam_next = 1.0
        window = []          # step norms of the recent full steps at the floor
        step_inf = float("nan")
        be = float("nan")
        gate_failed = False
        clipped = 0

        def final_step(status, extra=""):
            """Take the converged step without evaluating there, as plain Newton did."""
            trial = x_flat - dx
            n_clip = bnd.project(trial, x_flat, dx) if bnd.active else 0
            x_flat[:] = trial
            history.append({"step_norm": step_inf, "damping": 1.0, "theta": float("nan"),
                            "clipped": n_clip})
            if callback is not None:
                callback(x, g_raw)
            if refresh is not None:
                refresh(x)
            if status == 1 and n_clip:
                return finish(8, False, ev, step_inf, be, f"{n_clip} components held by a bound")
            return finish(status, True, ev, step_inf, be, extra)

        for it in range(int(maxfev)):
            g_raw, g, jac = ev
            state["ev"] = ev
            last_it = it == int(maxfev) - 1
            try:
                solve, r = lin.factorize(jac)
                nfact += 1
                dx = np.asarray(solve(g_raw if lin.kind == "callable" else g),
                                dtype=float).reshape(-1)
            except _SingularJacobian as exc:
                return finish(5, False, ev, step_inf, float("nan"), str(exc))
            except _LinearSolverFailed as exc:
                return finish(6, False, ev, step_inf, float("nan"), str(exc), krylov=True)
            if not np.all(np.isfinite(dx)):
                return finish(6, False, ev, step_inf, float("nan"), "non-finite Newton step")

            dy = dx / d
            step_inf = float(np.max(np.abs(dy))) if n else 0.0
            y = x_flat / d
            if relative:
                limit = tol_vec + rtol * np.abs(y)
                converged = bool(np.all(np.abs(dy) <= limit))
                with np.errstate(divide="ignore", invalid="ignore"):
                    excess = float(np.max(np.where(dy == 0.0, 0.0, np.abs(dy) / limit)))
            else:
                converged = step_inf < tol
                excess = step_inf / tol if tol > 0 else (0.0 if step_inf == 0 else np.inf)
            if not legacy_exact:
                converged = converged or step_inf == 0.0
            near = converged or (refresh is None and excess < _NEAR)
            state["step"] = step_inf
            state["last"] = converged or last_it

            # The verdict uses the residual at x, before the step: no evaluation
            # beyond those of plain Newton. Near a solution the step only improves it.
            be = float("nan")
            if near or last_it or relative:
                be = backward_error(g, jac)
            at_floor = near
            gate = backward_tol is None or np.isnan(be) or be <= backward_tol
            stagnant = (use_stagnation and at_floor and len(window) >= _STAGNATION_WINDOW
                        and step_inf >= _STAGNATION_RATIO * min(window[-_STAGNATION_WINDOW:]))

            theta = float("nan")
            if mode == "none":
                # Plain (or bound-shortened) step; callback and refresh before the
                # next evaluation, as the callers of the undamped iteration expect.
                lam = 1.0
                if not near and bnd.active:
                    lam = max(_LAM_FLOOR, bnd.max_step(x_flat, dx))
                trial = x_flat - lam * dx
                clipped = bnd.project(trial, x_flat, dx) if bnd.active else 0
                x_flat[:] = trial
                history.append({"step_norm": step_inf, "damping": lam, "theta": theta,
                                "clipped": clipped})
                if callback is not None:
                    callback(x, g_raw)
                if refresh is not None:
                    refresh(x)
                if relative and step_inf > 0.0:
                    # The relative test uses x after the step (and the callback).
                    converged = bool(np.all(np.abs(dy) <= tol_vec + rtol * np.abs(x_flat / d)))
                if converged and gate:
                    return finish(0, True, ev, step_inf, be)
                if stagnant and gate:
                    if clipped:
                        return finish(8, False, ev, step_inf, be,
                                      f"{clipped} components held by a bound")
                    return finish(1, True, ev, step_inf, be,
                                  f"|dx| = {step_inf:.2e} (tol {np.max(tol):.1e})")
                gate_failed = converged
                if last_it:
                    break
                ev_new = evaluate(x, guard=False)
                if ev_new is None:
                    return finish(4, False, ev, step_inf, float("nan"), "after a full step")
                ev = ev_new
            else:
                if converged and gate:
                    return final_step(0)
                if stagnant and gate:
                    if clipped:
                        return finish(8, False, ev, step_inf, be,
                                      f"{clipped} components held by a bound")
                    return final_step(1, f"|dx| = {step_inf:.2e} (tol {np.max(tol):.1e})")
                gate_failed = converged
                accepted = None
                lam_max = max(_LAM_FLOOR, bnd.max_step(x_flat, dx)) if bnd.active else 1.0
                at_lam_max = None   # (trial, ev_t, clipped) of a trial at lam_max, if made
                if mode == "guarded":
                    # Full step (shortened only by the bounds far from the solution).
                    lam = 1.0 if near else lam_max
                    trial = x_flat - lam * dx
                    clipped = bnd.project(trial, x_flat, dx) if bnd.active else 0
                    ev_t = evaluate(trial.reshape(shape), guard=True)
                    if lam == lam_max:
                        at_lam_max = (trial, ev_t, clipped)
                    if ev_t is not None:
                        accepted = (trial, ev_t, lam)
                    else:
                        lam_next = 0.25 * lam
                if accepted is None:
                    # Damped search: monotonicity test or Armijo, from lam_next.
                    lam = min(lam_next, lam_max)
                    dy_rms = _rms(dy)
                    row = r if r is not None else (_row_scale(jac) if _is_matrix(jac) else 1.0)
                    phi0 = float(np.linalg.norm(row * g))
                    best = None
                    # Near the solution a failed test is usually round-off: search briefly.
                    lam_min = _LAM_NEAR if near else _LAM_MIN
                    while lam >= lam_min:
                        trial = x_flat - lam * dx
                        clipped = bnd.project(trial, x_flat, dx) if bnd.active else 0
                        ev_t = evaluate(trial.reshape(shape), guard=True)
                        if lam == lam_max:
                            at_lam_max = (trial, ev_t, clipped)
                        if ev_t is None:
                            lam *= 0.25
                            continue
                        if mode == "armijo":
                            phi = float(np.linalg.norm(row * ev_t[1]))
                            if phi <= (1.0 - _ARMIJO_C * lam) * phi0:
                                accepted = (trial, ev_t, lam)
                                break
                            if best is None or phi < best[0]:
                                best = (phi, trial, ev_t, lam, clipped)
                            lam *= 0.5
                            continue
                        try:
                            rhs = ev_t[0] if lin.kind == "callable" else ev_t[1]
                            dbar = np.asarray(solve(rhs), dtype=float).reshape(-1) / d
                        except _LinearSolverFailed:
                            dbar = np.full(n, np.inf)    # no test possible: reject the trial
                        theta = _rms(dbar) / dy_rms if dy_rms > 0.0 else 0.0
                        if not np.isfinite(theta):
                            lam *= 0.5
                            continue
                        if theta <= 1.0 - lam / 4.0:
                            accepted = (trial, ev_t, lam)
                            break
                        mu = 0.5 * dy_rms * lam**2 / max(_rms(dbar - (1.0 - lam) * dy), 1.0e-300)
                        lam = min(0.5 * lam, max(mu, 0.1 * lam))
                    if accepted is None and best is not None and best[0] < phi0:
                        _, trial, ev_t, lam, clipped = best
                        ev_t = evaluate(trial.reshape(shape), guard=True)  # restore model state
                        if ev_t is not None:
                            accepted = (trial, ev_t, lam)
                    escaped = False
                    if accepted is None and _ESCAPE:
                        lam = lam_max
                        if at_lam_max is not None:
                            trial, ev_t, clipped = at_lam_max
                            if ev_t is not None:
                                ev_t = evaluate(trial.reshape(shape), guard=True)
                        else:
                            trial = x_flat - lam * dx
                            clipped = bnd.project(trial, x_flat, dx) if bnd.active else 0
                            ev_t = evaluate(trial.reshape(shape), guard=True)
                        if ev_t is not None:
                            accepted = (trial, ev_t, lam)
                            escaped = True
                    if accepted is None:
                        extra = f"{lam_min:g} at iteration {it}"
                        if clipped:
                            extra += f"; {clipped} components held by a bound"
                        return finish(3, False, ev, step_inf, backward_error(g, jac), extra)
                    lam_next = 1.0 if (escaped or mode == "guarded") else min(1.0, 4.0 * accepted[2])

                trial, ev, lam = accepted
                x_flat[:] = trial
                history.append({"step_norm": step_inf, "damping": lam, "theta": theta,
                                "clipped": clipped})
                stale = False
                if callback is not None:
                    # The callback may change x or model state: re-evaluate after it.
                    callback(x, g_raw)
                    stale = True
                if refresh is not None:
                    refresh(x)
                    stale = True
                if stale:
                    ev_new = evaluate(x, guard=True)
                    if ev_new is None:
                        return finish(4, False, ev, step_inf, float("nan"),
                                      "after the callback or refresh")
                    ev = ev_new
            if verbose:
                print(f"newton it={it:3d} |dx|={step_inf:.3e} lam={lam:.3g} "
                      f"theta={theta:.3g} clipped={clipped} nfev={nfev}")
            if stagnant:
                window.clear()      # the backward error did not pass: keep iterating
            elif use_stagnation and at_floor:
                # The Newton step norm, damped or not: near the floor the damping
                # test fails on round-off, and a damped step must not reset the window.
                window.append(step_inf)
            else:
                window.clear()

        if mode != "none":
            be = backward_error(ev[1], ev[2])     # ev is at x after a damped step
        if gate_failed:
            return finish(7, False, ev, step_inf, be, f"{be:.2e} after maxfev iterations")
        if clipped:
            return finish(8, False, ev, step_inf, be, f"{clipped} components held by a bound")
        return finish(2, False, ev, step_inf, be)

    try:
        return iterate()
    except _LastEvaluationFailed as exc:
        return finish(2, False, state["ev"], state["step"], float("nan"),
                      f"the residual at the last trial point raised {exc}")
```
