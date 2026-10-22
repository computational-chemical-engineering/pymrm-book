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

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/solve.py#L40-L53)

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
