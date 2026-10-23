# `pymrm.convect.minmod`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`minmod(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the Minmod TVD correction in normalized-variable space.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L430-L439)

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
