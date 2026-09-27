# `pymrm.checks.find_roots`

[Back to module page](../modules/pymrm.checks) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`find_roots(f, lo, hi, n_scan = 64, log = False, xtol = 1e-12)`

## Summary

Locate every sign change of ``f`` on ``[lo, hi]`` and refine each root.

## Documentation

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

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/checks.py#L155-L204)

```python
def find_roots(f, lo, hi, n_scan=64, log=False, xtol=1e-12):
    """Locate every sign change of ``f`` on ``[lo, hi]`` and refine each root.

    Parameters
    ----------
    f : callable
        Scalar function. It may raise, or return ``nan``, where the underlying
        model cannot be evaluated; such points are reported, never taken as a
        sign.
    lo, hi : float
        Physically possible range.
    n_scan : int, optional
        Number of scan points.
    log : bool, optional
        Scan on a logarithmic grid (``lo`` and ``hi`` must be positive).
    xtol : float, optional
        Absolute tolerance of each refined root (``brentq`` ``xtol``).

    Returns
    -------
    dict
        ``roots`` (sorted list), ``failed`` (scan points where ``f`` could not
        be evaluated) and ``message``. No sign change gives an empty list and
        says so; it does NOT widen the range.
    """
    grid = np.geomspace(lo, hi, n_scan) if log else np.linspace(lo, hi, n_scan)

    def safe(x):
        try:
            value = float(f(x))
        except Exception:  # noqa: BLE001 - a failed model evaluation is data here
            return float("nan")
        return value

    values = np.array([safe(x) for x in grid])
    failed = [float(x) for x, v in zip(grid, values) if not np.isfinite(v)]
    roots = [float(x) for x, v in zip(grid, values) if v == 0.0]
    for (x1, v1), (x2, v2) in zip(zip(grid, values), zip(grid[1:], values[1:])):
        if np.isfinite(v1) and np.isfinite(v2) and v1 * v2 < 0.0:
            roots.append(float(brentq(safe, x1, x2, xtol=xtol)))
    roots.sort()
    if not roots:
        message = "no sign change in the scanned range"
    elif len(roots) > 1:
        message = f"{len(roots)} roots: multiplicity, report all of them"
    else:
        message = "one root"
    if failed:
        message += f"; f could not be evaluated at {len(failed)} scan points"
    return {"roots": roots, "failed": failed, "message": message}
```
