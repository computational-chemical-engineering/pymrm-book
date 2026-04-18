# `pymrm.convect.muscl`

## Signature

`pymrm.convect.muscl(normalized_c_c, normalized_x_c, normalized_x_d)`

## Docstring

```text
Compute the MUSCL TVD correction in normalized-variable space.
```

## Implementation

```python
def muscl(normalized_c_c, normalized_x_c, normalized_x_d):
    """Compute the MUSCL TVD correction in normalized-variable space."""
    normalized_concentration_diff = np.maximum(
        0,
        np.where(
            normalized_c_c < normalized_x_c / (2 * normalized_x_d),
            ((2 * normalized_x_d - normalized_x_c) / normalized_x_c - 1)
            * normalized_c_c,  # noqa: E501
            np.where(
                normalized_c_c < 1 + normalized_x_c - normalized_x_d,
                normalized_x_d - normalized_x_c,
                1 - normalized_c_c,
            ),
        ),
    )  # noqa: E501
    return normalized_concentration_diff

```
