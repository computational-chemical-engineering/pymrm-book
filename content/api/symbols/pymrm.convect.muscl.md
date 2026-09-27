# `pymrm.convect.muscl`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`muscl(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the MUSCL TVD correction in normalized-variable space.

## Documentation

Uniform grid: 2 c_c up to 1/4, c_c + 1/4 up to 3/4, then 1.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L456-L475)

```python
def muscl(normalized_c_c, normalized_x_c, normalized_x_d):
    """Compute the MUSCL TVD correction in normalized-variable space.

    Uniform grid: 2 c_c up to 1/4, c_c + 1/4 up to 3/4, then 1.
    """
    normalized_concentration_diff = np.maximum(
        0,
        np.where(
            # the first line meets c_c + x_d - x_c at c_c = x_c / 2
            normalized_c_c < normalized_x_c / 2,
            ((2 * normalized_x_d - normalized_x_c) / normalized_x_c - 1)
            * normalized_c_c,  # noqa: E501
            np.where(
                normalized_c_c < 1 + normalized_x_c - normalized_x_d,
                normalized_x_d - normalized_x_c,
                1 - normalized_c_c,
            ),
        ),
    )  # noqa: E501
    return normalized_concentration_diff
```
