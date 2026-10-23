# `pymrm.solve.KrylovBreakdown`

[Back to module page](../modules/pymrm.solve) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`KrylovBreakdown(message, result = None)`

## Summary

An iterative linear solver did not converge (status 6).

## Documentation

Also a ``RuntimeError``, as raised up to pymrm 2.5.0.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/solve.py#L57-L61)

```python
class KrylovBreakdown(NewtonBreakdown, RuntimeError):
    """An iterative linear solver did not converge (status 6).

    Also a ``RuntimeError``, as raised up to pymrm 2.5.0.
    """
```

## Members

### `__init__(message, result = None)`

Initialize self.  See help(type(self)) for accurate signature.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/solve.py#L52-L54)
