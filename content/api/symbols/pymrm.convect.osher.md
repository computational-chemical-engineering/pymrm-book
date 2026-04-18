# `pymrm.convect.osher`

## Signature

`pymrm.convect.osher(normalized_c_c, normalized_x_c, normalized_x_d)`

## Docstring

```text
Compute the Osher TVD correction in normalized-variable space.
```

## Implementation

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
