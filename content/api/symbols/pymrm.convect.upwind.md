# `pymrm.convect.upwind`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`upwind(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Return zero correction (first-order upwind limiter).

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L392-L395)

```python
def upwind(normalized_c_c, normalized_x_c, normalized_x_d):
    """Return zero correction (first-order upwind limiter)."""
    normalized_concentration_diff = np.zeros_like(normalized_c_c)
    return normalized_concentration_diff
```
