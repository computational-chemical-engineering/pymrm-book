# `pymrm.solve.KrylovBreakdown`

[Back to module page](../modules/pymrm.solve) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`KrylovBreakdown(message, result = None)`

## Summary

An iterative linear solver did not converge (status 6).

## Documentation

Also a ``RuntimeError``, as raised up to pymrm 2.5.0.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L57-L61)

```python
class KrylovBreakdown(NewtonBreakdown, RuntimeError):
    """An iterative linear solver did not converge (status 6).

    Also a ``RuntimeError``, as raised up to pymrm 2.5.0.
    """
```

## Members

### `__init__(message, result = None)`

Initialize self.  See help(type(self)) for accurate signature.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L52-L54)

### `__delattr__()`

Implement delattr(self, name).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__dir__()`

Default dir() implementation.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__eq__()`

Return self==value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__format__()`

Default object formatter.

Return str(self) if format_spec is empty. Raise TypeError otherwise.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__ge__()`

Return self>=value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__getattribute__()`

Return getattr(self, name).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__getstate__()`

Helper for pickle.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__gt__()`

Return self>value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__hash__()`

Return hash(self).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__le__()`

Return self<=value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__lt__()`

Return self<value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__ne__()`

Return self!=value.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__new__()`

Create and return a new object.  See help(type) for accurate signature.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__reduce__()`

Helper for pickle.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__reduce_ex__()`

Helper for pickle.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__repr__()`

Return repr(self).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__setattr__()`

Implement setattr(self, name, value).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__setstate__()`

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__sizeof__()`

Size of object in memory, in bytes.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__str__()`

Return str(self).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `__subclasshook__()`

Abstract classes can override this to customize issubclass().

This is invoked early on by abc.ABCMeta.__subclasscheck__().
It should return True, False or NotImplemented.  If it returns
NotImplemented, the normal algorithm is used.  Otherwise, it
overrides the normal algorithm (and the outcome is cached).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `add_note()`

Exception.add_note(note) -- add a note to the exception

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)

### `with_traceback()`

Exception.with_traceback(tb) -- set self.__traceback__ to tb and return self.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/519353229140eeec75a2a29f225cdc3e35aa5e4f/src/pymrm/solve.py#L0-L0)
