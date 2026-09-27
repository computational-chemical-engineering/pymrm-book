# `pymrm.convect.osher`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`osher(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the Osher TVD correction in normalized-variable space.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L430-L440)

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
