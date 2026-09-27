# `pymrm.checks.observed_orders`

[Back to module page](../modules/pymrm.checks) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`observed_orders(solve, ns, ratio = None)`

## Summary

Run a refinement study and report observed orders of convergence.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/checks.py#L98-L152)

```python
def observed_orders(solve, ns, ratio=None):
    """Run a refinement study and report observed orders of convergence.

    Parameters
    ----------
    solve : callable
        ``solve(n) -> float or array``, the quantity of interest computed with
        resolution ``n`` (cells, or number of time steps). An array must have
        the same shape at every resolution (for example values at fixed
        positions).
    ns : sequence[int]
        At least three resolutions with a constant refinement ratio, for example
        ``(50, 100, 200, 400)``.
    ratio : float, optional
        Refinement ratio; default ``ns[1] / ns[0]``.

    Returns
    -------
    dict
        ``values`` per resolution, ``orders`` from each consecutive triple,
        ``extrapolated`` (Richardson estimate from the finest triple) and
        ``error_estimate`` of the finest value against it; ``nan`` when the
        finest order is not positive (the study is not converging).

    Notes
    -----
    The order from values ``q1, q2, q3`` on successively finer grids is
    ``log(|q1 - q2| / |q2 - q3|) / log(ratio)``; it needs no exact solution. An
    order far from the expected one means the study is not in the asymptotic
    range, the refinement does not control the error that dominates, or there is
    a bug. For a non-uniform grid, refine it in a nested way (see the pymrm
    agent plugin's profiles.md).
    """
    ns = list(ns)
    if len(ns) < 3:
        raise ValueError("observed_orders needs at least three resolutions")
    ratio = float(ratio if ratio is not None else ns[1] / ns[0])
    if not np.allclose(np.array(ns[1:], dtype=float) / np.array(ns[:-1], dtype=float), ratio):
        raise ValueError("observed_orders needs a constant refinement ratio between resolutions")
    values = [np.asarray(solve(n), dtype=float) for n in ns]
    orders = []
    for q1, q2, q3 in zip(values, values[1:], values[2:]):
        d1, d2 = np.max(np.abs(q1 - q2)), np.max(np.abs(q2 - q3))
        orders.append(float(math.log(d1 / d2) / math.log(ratio)) if d1 > 0 and d2 > 0 else float("nan"))
    p = orders[-1]
    q_prev, q_last = values[-2], values[-1]
    if np.isfinite(p) and p > 0:
        extrapolated = q_last + (q_last - q_prev) / (ratio**p - 1.0)
        error_estimate = float(np.max(np.abs(q_last - extrapolated)))
    else:  # not converging (or exactly converged): no error estimate
        extrapolated = q_last
        error_estimate = float("nan")
    as_out = (lambda v: float(v)) if values[0].ndim == 0 else (lambda v: v)
    return {"values": [as_out(v) for v in values], "orders": orders,
            "extrapolated": as_out(extrapolated), "error_estimate": error_estimate}
```
