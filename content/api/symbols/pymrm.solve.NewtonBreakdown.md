# `pymrm.solve.NewtonBreakdown`

[Back to module page](../modules/pymrm.solve) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`NewtonBreakdown(message, result = None)`

## Summary

Raised by `newton` when no Newton step can be formed.

## Documentation

A singular Jacobian (status 5), a non-finite residual or Jacobian that no
damping can avoid (status 4) or a non-finite Newton step (status 6). It is
a ``LinAlgError`` and so a ``ValueError``, as the exceptions these cases
raised up to pymrm 2.5.0. ``result`` holds the
`scipy.optimize.OptimizeResult` with the status and the last
iterate ``x``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/solve.py#L41-L54)

```python
class NewtonBreakdown(np.linalg.LinAlgError):
    """Raised by :func:`newton` when no Newton step can be formed.

    A singular Jacobian (status 5), a non-finite residual or Jacobian that no
    damping can avoid (status 4) or a non-finite Newton step (status 6). It is
    a ``LinAlgError`` and so a ``ValueError``, as the exceptions these cases
    raised up to pymrm 2.5.0. ``result`` holds the
    :class:`scipy.optimize.OptimizeResult` with the status and the last
    iterate ``x``.
    """

    def __init__(self, message, result=None):
        super().__init__(message)
        self.result = result
```

## Members

### `__init__(message, result = None)`

Initialize self.  See help(type(self)) for accurate signature.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/solve.py#L52-L54)
