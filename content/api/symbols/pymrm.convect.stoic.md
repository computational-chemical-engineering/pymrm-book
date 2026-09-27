# `pymrm.convect.stoic`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`stoic(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the STOIC TVD correction in normalized-variable space.

## Documentation

Piecewise: the SMART line ``c_f = k c_c`` up to its intersection with the
central-difference line, then central differencing up to ``c_c = x_c``,
then QUICK, then ``c_f = 1``. On a uniform grid (``x_c = 1/2``,
``x_d = 3/4``) this is 3 c_c, (1 + c_c)/2, 3/8 + 3 c_c/4 and 1, with breaks
at 1/5, 1/2 and 5/6.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L512-L541)

```python
def stoic(normalized_c_c, normalized_x_c, normalized_x_d):
    """Compute the STOIC TVD correction in normalized-variable space.

    Piecewise: the SMART line ``c_f = k c_c`` up to its intersection with the
    central-difference line, then central differencing up to ``c_c = x_c``,
    then QUICK, then ``c_f = 1``. On a uniform grid (``x_c = 1/2``,
    ``x_d = 3/4``) this is 3 c_c, (1 + c_c)/2, 3/8 + 3 c_c/4 and 1, with breaks
    at 1/5, 1/2 and 5/6.
    """
    x_c = normalized_x_c
    x_d = normalized_x_d
    c_c = normalized_c_c
    slope = x_d * (1 - 3 * x_c + 2 * x_d) / (x_c * (1 - x_c))
    # intersection of c_f = slope * c_c with the central-difference line
    c_break = x_c / (1 + 2 * x_d)
    c_f = np.where(
        c_c < c_break,
        slope * c_c,
        np.where(
            c_c < x_c,
            (x_d - x_c + (1 - x_d) * c_c) / (1 - x_c),
            np.where(
                c_c < x_c / x_d * (1 + x_d - x_c),
                (x_d * (x_d - x_c) + x_d * (1 - x_d) / x_c * c_c) / (1 - x_c),
                1.0,
            ),
        ),
    )
    normalized_concentration_diff = np.maximum(0, c_f - c_c)
    return normalized_concentration_diff
```
