# `pymrm.convect.minmod`

## Signature

`pymrm.convect.minmod(normalized_c_c, normalized_x_c, normalized_x_d)`

## Docstring

```text
Compute the Minmod TVD correction in normalized-variable space.
```

## Implementation

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
