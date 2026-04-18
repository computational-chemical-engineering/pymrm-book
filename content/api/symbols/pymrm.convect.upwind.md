# `pymrm.convect.upwind`

## Signature

`pymrm.convect.upwind(normalized_c_c, normalized_x_c, normalized_x_d)`

## Docstring

```text
Return zero correction (first-order upwind limiter).
```

## Implementation

```python
def upwind(normalized_c_c, normalized_x_c, normalized_x_d):
    """Return zero correction (first-order upwind limiter)."""
    normalized_concentration_diff = np.zeros_like(normalized_c_c)
    return normalized_concentration_diff

```
