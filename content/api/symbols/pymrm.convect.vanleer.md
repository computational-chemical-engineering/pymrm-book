# `pymrm.convect.vanleer`

## Signature

`pymrm.convect.vanleer(normalized_c_c, normalized_x_c, normalized_x_d)`

## Docstring

```text
Compute the van-Leer TVD correction in normalized-variable space.
```

## Implementation

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
