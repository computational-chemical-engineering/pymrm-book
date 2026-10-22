# `pymrm.solve.continuation`

[Back to module page](../modules/pymrm.solve) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`continuation(function, initial_guess, params, *, max_halvings = 6, max_change = 0.2, newton_kwargs = None, verbose = 0)`

## Summary

Solve ``function(x, p) = 0`` along a sequence of parameter values.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L1046-L1142)

```python
def continuation(function, initial_guess, params, *, max_halvings=6, max_change=0.2,
                 newton_kwargs=None, verbose=0):
    """Solve ``function(x, p) = 0`` along a sequence of parameter values.

    Natural-parameter continuation: each point starts from a secant
    extrapolation of the two previous solutions and is corrected with
    :func:`newton`. A failed correction halves the parameter step (at most
    ``max_halvings`` times per requested value). A correction that moves
    ``x`` by more than ``max_change`` times ``max |x|`` from the prediction
    counts as failed: near a turning point (fold) the corrector otherwise
    jumps silently to another solution branch. The march then stops and
    reports where; the fold lies between the last parameter reached and the
    next one. Following a branch around a fold needs arclength continuation,
    which this function does not do.

    Parameters
    ----------
    function : callable
        ``function(x, p) -> (residual, jacobian)``.
    initial_guess : numpy.ndarray
        Guess for the first parameter value.
    params : sequence of float
        Parameter values, in the order to visit them.
    max_halvings : int, optional
        Largest number of step halvings on the way to one parameter value.
    max_change : float or None, optional
        Largest accepted relative distance between prediction and solution;
        ``None`` disables the branch-jump check.
    newton_kwargs : dict, optional
        Options for :func:`newton`.
    verbose : int, optional
        ``1`` prints one line per accepted point.

    Returns
    -------
    scipy.optimize.OptimizeResult
        ``success`` (every value reached), ``message``, ``params`` (the values
        reached), ``xs`` (their solutions), ``results`` (their :func:`newton`
        results), ``last_param`` (the last parameter at which a solution was
        found, possibly an intermediate one) and ``x`` (that solution).
    """
    params = [float(p) for p in params]
    options = dict(newton_kwargs or {})
    first = _attempt(lambda xv: function(xv, params[0]), np.array(initial_guess, dtype=float),
                     (), options)
    if not first.success:
        return OptimizeResult(x=first.x, success=False, params=[], xs=[], results=[first],
                              last_param=None,
                              message=f"no solution at the first value {params[0]:g}: "
                                      f"{first.message}")
    done, xs, results = [params[0]], [first.x.copy()], [first]
    path_p, path_x = [params[0]], [first.x.copy()]
    for target in params[1:]:
        if target == path_p[-1]:            # a repeated value: nothing to solve
            done.append(target)
            xs.append(path_x[-1].copy())
            results.append(results[-1])
            continue
        halvings = 0
        p = target
        while True:
            if len(path_p) >= 2:
                ratio = (p - path_p[-1]) / (path_p[-1] - path_p[-2])
                guess = path_x[-1] + ratio * (path_x[-1] - path_x[-2])
            else:
                guess = path_x[-1].copy()
            res = _attempt(lambda xv, _p=p: function(xv, _p), guess, (), options)
            jumped = False
            if res.success and max_change is not None and len(path_p) >= 2:
                # no prediction to compare with before the second point
                size = max(float(np.max(np.abs(path_x[-1]))), float(np.max(np.abs(res.x))),
                           np.finfo(float).tiny)
                jumped = float(np.max(np.abs(res.x - guess))) > max_change * size
            if res.success and not jumped:
                path_p.append(p)
                path_x.append(res.x.copy())
                if verbose:
                    print(f"continuation p={p:g} nit={res.nit}")
                if p == target:
                    done.append(target)
                    xs.append(res.x.copy())
                    results.append(res)
                    break
                p = target
                continue
            halvings += 1
            if halvings > max_halvings:
                why = ("the corrector jumps to another solution branch" if jumped
                       else f"the corrector fails ({res.message})")
                return OptimizeResult(
                    x=path_x[-1], success=False, params=done, xs=xs, results=results,
                    last_param=path_p[-1],
                    message=f"stopped at p = {path_p[-1]:g} on the way to {target:g}: {why}; "
                            "probably a turning point (fold) of the solution branch")
            p = path_p[-1] + 0.5 * (p - path_p[-1])
    return OptimizeResult(x=path_x[-1], success=True, params=done, xs=xs, results=results,
                          last_param=path_p[-1], message="Reached every parameter value")
```
