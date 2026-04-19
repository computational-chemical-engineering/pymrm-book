# `pymrm.convect.osher`

[Back to module page](../modules/pymrm.convect.md) · [Back to alphabetical overview](../alphabetical_overview.md)

## Signature

`osher(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the Osher TVD correction in normalized-variable space.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L410-L420)

```python
def osher(normalized_c_c, normalized_x_c, normalized_x_d):
    """Compute the Osher TVD correction in normalized-variable space."""
    normalized_concentration_diff = np.maximum(
        0,
        np.where(
            normalized_c_c < normalized_x_c / normalized_x_d,
            (normalized_x_d / normalized_x_c - 1) * normalized_c_c,
            1 - normalized_c_c,
        ),
    )
    return normalized_concentration_diff
```
