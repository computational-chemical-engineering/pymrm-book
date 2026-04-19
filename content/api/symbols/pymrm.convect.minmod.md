# `pymrm.convect.minmod`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`minmod(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the Minmod TVD correction in normalized-variable space.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L398-L407)

```python
def minmod(normalized_c_c, normalized_x_c, normalized_x_d):
    """Compute the Minmod TVD correction in normalized-variable space."""
    normalized_concentration_diff = np.maximum(
        0,
        (normalized_x_d - normalized_x_c)
        * np.minimum(
            normalized_c_c / normalized_x_c, (1 - normalized_c_c) / (1 - normalized_x_c)
        ),
    )
    return normalized_concentration_diff
```
