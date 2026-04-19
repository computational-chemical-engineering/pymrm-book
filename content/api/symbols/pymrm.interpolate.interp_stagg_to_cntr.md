# `pymrm.interpolate.interp_stagg_to_cntr`

[Back to module page](../modules/pymrm.interpolate.md) · [Back to alphabetical overview](../alphabetical_overview.md)

## Signature

`interp_stagg_to_cntr(staggered_values, x_f, x_c = None, axis = 0)`

## Summary

Interpolate face/staggered values to cell centers.

## Documentation

### Parameters

- `staggered_values` (*numpy.ndarray*)
  Values defined on staggered (face) locations.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates. If omitted, midpoint interpolation is used.

- `axis` (*int, optional*)
  Interpolation axis.

### Returns

- `numpy.ndarray`
  Cell-centered values with one fewer element along ``axis``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/interpolate.py#L9-L50)

```python
def interp_stagg_to_cntr(staggered_values, x_f, x_c=None, axis=0):
    """Interpolate face/staggered values to cell centers.

    Parameters
    ----------
    staggered_values : numpy.ndarray
        Values defined on staggered (face) locations.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates. If omitted, midpoint interpolation is used.
    axis : int, optional
        Interpolation axis.

    Returns
    -------
    numpy.ndarray
        Cell-centered values with one fewer element along ``axis``.
    """
    shape_f = list(staggered_values.shape)
    if axis < 0:
        axis += len(shape_f)
    shape_f_t = [
        math.prod(shape_f[:axis]),
        math.prod(shape_f[axis: axis + 1]),
        math.prod(shape_f[axis + 1:]),
    ]
    shape = shape_f.copy()
    shape[axis] -= 1
    staggered_values = np.reshape(staggered_values, shape_f_t)

    if x_c is None:
        cell_centered_values = 0.5 * (
            staggered_values[:, 1:, :] + staggered_values[:, :-1, :]
        )
    else:
        wght = (x_c - x_f[:-1]) / (x_f[1:] - x_f[:-1])
        cell_centered_values = staggered_values[:, :-1, :] + wght.reshape(
            (1, -1, 1)
        ) * (staggered_values[:, 1:, :] - staggered_values[:, :-1, :])

    return cell_centered_values.reshape(shape)
```
