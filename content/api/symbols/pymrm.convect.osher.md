# `pymrm.convect.osher`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`osher(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the Osher TVD correction in normalized-variable space.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/edd7b4da542580c2776cbb05bd6761bce4495f28/src/pymrm/convect.py#L442-L452)

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
