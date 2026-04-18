# `pymrm.grid.non_uniform_grid`

## Signature

`pymrm.grid.non_uniform_grid(left_bound, right_bound, num_points, dx_inf, factor)`

## Docstring

```text
Generate a one-dimensional stretched face grid.

Parameters
----------
left_bound, right_bound : float
    Domain bounds.
num_points : int
    Number of returned face coordinates, including both boundaries.
dx_inf : float
    Asymptotic cell width used in the stretching expression.
factor : float
    Geometric stretching factor. Values larger than ``1`` stretch cells;
    values between ``0`` and ``1`` compress cells.

Returns
-------
numpy.ndarray
    Monotonic array of face coordinates with length ``num_points``.
```

## Implementation

```python
def non_uniform_grid(left_bound, right_bound, num_points, dx_inf, factor):
    """Generate a one-dimensional stretched face grid.

    Parameters
    ----------
    left_bound, right_bound : float
        Domain bounds.
    num_points : int
        Number of returned face coordinates, including both boundaries.
    dx_inf : float
        Asymptotic cell width used in the stretching expression.
    factor : float
        Geometric stretching factor. Values larger than ``1`` stretch cells;
        values between ``0`` and ``1`` compress cells.

    Returns
    -------
    numpy.ndarray
        Monotonic array of face coordinates with length ``num_points``.
    """
    a = np.log(factor)
    unif = np.arange(num_points)
    b = np.exp(-a * unif)
    length = right_bound - left_bound
    c = (np.exp(a * (length / dx_inf - num_points + 1.0)) - b[-1]) / (1 - b[-1])
    x_f = left_bound + unif * dx_inf + np.log((1 - c) * b + c) * (dx_inf / a)
    return x_f

```
