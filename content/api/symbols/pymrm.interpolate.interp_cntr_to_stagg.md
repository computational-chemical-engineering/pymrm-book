# `pymrm.interpolate.interp_cntr_to_stagg`

## Signature

`pymrm.interpolate.interp_cntr_to_stagg(cell_centered_values, x_f, x_c=None, axis=0)`

## Docstring

```text
Interpolate cell-centered values to face/staggered locations.

Parameters
----------
cell_centered_values : numpy.ndarray
    Values defined at cell centers.
x_f : array_like
    Face coordinates along ``axis``.
x_c : array_like, optional
    Cell-center coordinates. If omitted, midpoint locations are used.
axis : int, optional
    Interpolation axis.

Returns
-------
numpy.ndarray
    Staggered values with one additional element along ``axis``.
```

## Implementation

```python
def interp_cntr_to_stagg(cell_centered_values, x_f, x_c=None, axis=0):
    """Interpolate cell-centered values to face/staggered locations.

    Parameters
    ----------
    cell_centered_values : numpy.ndarray
        Values defined at cell centers.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates. If omitted, midpoint locations are used.
    axis : int, optional
        Interpolation axis.

    Returns
    -------
    numpy.ndarray
        Staggered values with one additional element along ``axis``.
    """
    shape = list(cell_centered_values.shape)
    if axis < 0:
        axis += len(shape)
    shape_t = [
        math.prod(shape[:axis]),
        math.prod(shape[axis: axis + 1]),
        math.prod(shape[axis + 1:]),
    ]
    shape_f = shape.copy()
    shape_f[axis] += 1
    shape_f_t = shape_t.copy()
    shape_f_t[1] += 1
    if x_c is None:
        x_c = 0.5 * (x_f[:-1] + x_f[1:])

    wght = (x_f[1:-1] - x_c[:-1]) / (x_c[1:] - x_c[:-1])
    cell_centered_values = cell_centered_values.reshape(shape_t)
    if shape_t[1] == 1:
        staggered_values = np.tile(cell_centered_values, (1, 2, 1))
    else:
        staggered_values = np.empty(shape_f_t)
        staggered_values[:, 1:-1, :] = cell_centered_values[:, :-1, :] + wght.reshape(
            (1, -1, 1)
        ) * (cell_centered_values[:, 1:, :] - cell_centered_values[:, :-1, :])
        staggered_values[:, 0, :] = (
            cell_centered_values[:, 0, :] * (x_c[1] - x_f[0])
            - cell_centered_values[:, 1, :] * (x_c[0] - x_f[0])
        ) / (x_c[1] - x_c[0])
        staggered_values[:, -1, :] = (
            cell_centered_values[:, -1, :] * (x_f[-1] - x_c[-2])
            - cell_centered_values[:, -2, :] * (x_f[-1] - x_c[-1])
        ) / (x_c[-1] - x_c[-2])
    return staggered_values.reshape(shape_f)

```
