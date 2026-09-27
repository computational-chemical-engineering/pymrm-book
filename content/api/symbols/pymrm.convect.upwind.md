# `pymrm.convect.upwind`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`upwind(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Return zero correction (first-order upwind limiter).

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/b40fd3f7ac82d247ea864dca2aec0b8aa53589a1/src/pymrm/convect.py#L412-L415)

```python
def upwind(normalized_c_c, normalized_x_c, normalized_x_d):
    """Return zero correction (first-order upwind limiter)."""
    normalized_concentration_diff = np.zeros_like(normalized_c_c)
    return normalized_concentration_diff
```
