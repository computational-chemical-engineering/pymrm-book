# `pymrm.solve.pseudo_transient`

[Back to module page](../modules/pymrm.solve) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`pseudo_transient(function, initial_guess, mass = 1.0, dt = 0.001, args = (), *, dt_max = np.inf, max_steps = 200, growth = 10.0, steady_ratio = 0.1, steady_every = 10, newton_kwargs = None, steady_kwargs = None, verbose = 0)`

## Summary

Reach a steady state of ``function(x) = 0`` by implicit pseudo-time steps.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L950-L1067)

```python
def pseudo_transient(function, initial_guess, mass=1.0, dt=1e-3, args=(), *, dt_max=np.inf,
                     max_steps=200, growth=10.0, steady_ratio=0.1, steady_every=10,
                     newton_kwargs=None, steady_kwargs=None, verbose=0):
    """Reach a steady state of ``function(x) = 0`` by implicit pseudo-time steps.

    When Newton from the initial guess fails (ignition, extinction, a guess
    far from any solution), march ``mass dx/dt = -function(x)`` with implicit
    Euler steps instead: each step solves
    ``function(x) + mass (x - x_old) / dt = 0`` with :func:`newton`, which is
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

    Parameters
    ----------
    function : callable
        ``function(x, *args) -> (residual, jacobian)``, as for :func:`newton`,
        with a matrix Jacobian.
    initial_guess : numpy.ndarray
        Starting state.
    mass : float, numpy.ndarray or sparse matrix, optional
        Accumulation term: a scalar or an array broadcast against the state
        (a diagonal), or a matrix. It sets the relative speed of the fields in
        pseudo-time and must have the units of the residual per unit of the
        state; 1 suits residuals scaled like the state.
    dt : float, optional
        First pseudo-time step.
    args : tuple, optional
        Extra arguments of ``function``.
    dt_max : float, optional
        Largest pseudo-time step.
    max_steps : int, optional
        Largest number of accepted pseudo-time steps.
    growth : float, optional
        Largest factor by which ``dt`` grows per step.
    steady_ratio : float, optional
        Try the steady solve each time the residual norm has dropped by this
        factor.
    steady_every : int, optional
        Try the steady solve at least every so many steps.
    newton_kwargs : dict, optional
        Options for the Newton solve of each step (default ``maxfev=10``,
        ``damping="guarded"``).
    steady_kwargs : dict, optional
        Options for the steady Newton solves (default ``maxfev=30``,
        ``damping="guarded"``).
    verbose : int, optional
        ``1`` prints one line per step.

    Returns
    -------
    scipy.optimize.OptimizeResult
        ``x``, ``success``, ``message``, ``nsteps``, ``history`` (``dt``,
        residual norm and Newton iterations per step) and ``steady`` (the
        last steady :func:`newton` result).
    """
    x = np.array(initial_guess, dtype=float, order="C")
    shape = x.shape
    mass_matrix = _mass_matrix(mass, shape)
    inner = {"maxfev": 10, "damping": "guarded", **(newton_kwargs or {})}
    steady = {"maxfev": 30, "damping": "guarded", **(steady_kwargs or {})}
    history = []
    steady_result = None
    g_prev = None
    g_attempt = None

    def result(success, message, nsteps):
        xr = steady_result.x if (success and steady_result is not None) else x
        return OptimizeResult(x=xr, success=success, message=message, nsteps=nsteps,
                              history=history, steady=steady_result)

    for step in range(int(max_steps) + 1):
        g_now, _ = function(x, *args)
        g_norm = float(np.linalg.norm(np.asarray(g_now, dtype=float).ravel()))
        if not np.isfinite(g_norm):
            return result(False, "non-finite residual during the pseudo-time march", step)
        if (g_attempt is None or g_norm <= steady_ratio * g_attempt or step == max_steps
                or (steady_every and step % steady_every == 0)):
            g_attempt = g_norm
            steady_result = _attempt(function, x, args, steady)
            if steady_result.success:
                return result(True, f"Converged by the steady Newton solve after {step} "
                              "pseudo-time steps", step)
            if step == max_steps:
                break
        if g_prev is not None and g_norm > 0.0 and history and history[-1]["nit"] <= 3:
            dt = min(dt_max, dt * min(growth, max(2.0, g_prev / g_norm)))
        g_prev = g_norm
        x_old = x.ravel().copy()
        for _ in range(20):
            def transient(xv, *a, _dt=dt):
                g, jac = function(xv, *a)
                g = np.asarray(g, dtype=float).ravel() + mass_matrix @ (xv.ravel() - x_old) / _dt
                return g, jac + mass_matrix / _dt
            step_result = _attempt(transient, x, args, inner)
            if step_result.success:
                break
            dt *= 0.25
        else:
            return result(False, f"pseudo-time step {step} failed down to dt = {dt:.2e}", step)
        x = step_result.x
        history.append({"dt": dt, "residual_norm": g_norm, "nit": step_result.nit})
        if verbose:
            print(f"pseudo_transient step {step}: dt={dt:.2e} |g|={g_norm:.2e} "
                  f"nit={step_result.nit}")
    return result(False, "max_steps reached without a converged steady solve", int(max_steps))
```
