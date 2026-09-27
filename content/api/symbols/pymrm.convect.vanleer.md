# `pymrm.convect.vanleer`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`vanleer(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the van-Leer TVD correction in normalized-variable space.

## Documentation

The curve is the parabola through (0, 0), (x_c, x_d) and (1, 1). It rises
above ``c_f = 1`` when ``x_d - x_c > x_c (1 - x_c)``, for example next to a
boundary where the upstream point is a face half a cell away (x_c = 1/3,
x_d = 2/3); the correction is capped at ``1 - c_c`` to stay bounded. The
cap acts only above c_c = x_c and does not reduce the order.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L544-L563)

```python
def vanleer(normalized_c_c, normalized_x_c, normalized_x_d):
    """Compute the van-Leer TVD correction in normalized-variable space.

    The curve is the parabola through (0, 0), (x_c, x_d) and (1, 1). It rises
    above ``c_f = 1`` when ``x_d - x_c > x_c (1 - x_c)``, for example next to a
    boundary where the upstream point is a face half a cell away (x_c = 1/3,
    x_d = 2/3); the correction is capped at ``1 - c_c`` to stay bounded. The
    cap acts only above c_c = x_c and does not reduce the order.
    """
    normalized_concentration_diff = np.maximum(
        0,
        np.minimum(
            normalized_c_c
            * (1 - normalized_c_c)
            * (normalized_x_d - normalized_x_c)
            / (normalized_x_c * (1 - normalized_x_c)),
            1 - normalized_c_c,
        ),
    )
    return normalized_concentration_diff
```
