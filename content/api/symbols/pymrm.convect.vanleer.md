# `pymrm.convect.vanleer`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`vanleer(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the van-Leer TVD correction in normalized-variable space.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L537-L546)

```python
def vanleer(normalized_c_c, normalized_x_c, normalized_x_d):
    """Compute the van-Leer TVD correction in normalized-variable space."""
    normalized_concentration_diff = np.maximum(
        0,
        normalized_c_c
        * (1 - normalized_c_c)
        * (normalized_x_d - normalized_x_c)
        / (normalized_x_c * (1 - normalized_x_c)),
    )
    return normalized_concentration_diff
```
