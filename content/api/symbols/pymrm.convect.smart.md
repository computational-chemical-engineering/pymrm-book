# `pymrm.convect.smart`

## Signature

`pymrm.convect.smart(normalized_c_c, normalized_x_c, normalized_x_d)`

## Docstring

```text
Compute the SMART TVD correction in normalized-variable space.
```

## Implementation

```python
def smart(normalized_c_c, normalized_x_c, normalized_x_d):
    """Compute the SMART TVD correction in normalized-variable space."""
    normalized_concentration_diff = np.maximum(
        0,
        np.where(
            normalized_c_c < normalized_x_c / 3,
            (
                normalized_x_d
                * (1 - 3 * normalized_x_c + 2 * normalized_x_d)
                / (normalized_x_c * (1 - normalized_x_c))
                - 1
            )
            * normalized_c_c,  # noqa: E501
            np.where(
                normalized_c_c
                < normalized_x_c
                / normalized_x_d
                * (1 + normalized_x_d - normalized_x_c),  # noqa: E501
                (
                    normalized_x_d * (normalized_x_d - normalized_x_c)  # noqa: E501
                    + normalized_x_d
                    * (1 - normalized_x_d)
                    / normalized_x_c
                    * normalized_c_c
                )
                / (1 - normalized_x_c)
                - normalized_c_c,
                1 - normalized_c_c,
            ),
        ),
    )  # noqa: E501
    return normalized_concentration_diff

```
