# `pymrm.interpolate.create_staggered_array`

## Signature

`pymrm.interpolate.create_staggered_array(array, shape, axis, x_f=None, x_c=None)`

## Docstring

```text
Create a face/staggered field from scalar, centered, or staggered input.

Parameters
----------
array : array_like
    Input values. May be scalar, centered, or already staggered.
shape : tuple[int, ...] or int
    Target centered-field shape.
axis : int
    Staggering axis.
x_f, x_c : array_like, optional
    Face and center coordinates used when centered input must be
    interpolated to faces.

Returns
-------
numpy.ndarray
    Broadcasted/interpolated array with staggered shape.
```

## Implementation

```python
def create_staggered_array(array, shape, axis, x_f=None, x_c=None):
    """Create a face/staggered field from scalar, centered, or staggered input.

    Parameters
    ----------
    array : array_like
        Input values. May be scalar, centered, or already staggered.
    shape : tuple[int, ...] or int
        Target centered-field shape.
    axis : int
        Staggering axis.
    x_f, x_c : array_like, optional
        Face and center coordinates used when centered input must be
        interpolated to faces.

    Returns
    -------
    numpy.ndarray
        Broadcasted/interpolated array with staggered shape.
    """
    if not isinstance(shape, (list, tuple)):
        shape_f = [shape]
    else:
        shape_f = list(shape)
    if axis < 0:
        axis += len(shape)
    shape_f[axis] += 1
    shape_f = tuple(shape_f)

    array = np.asarray(array)
    if array.shape == shape_f:
        return array
    if array.size == 1:
        array = np.full(shape_f, array)
        return array

    if len(shape) != 1 and array.ndim == 1:
        shape_new = [1] * len(shape)
        if array.size in (shape[axis], shape_f[axis]):
            shape_new[axis] = -1
        else:
            for i in range(len(shape) - 1, -1, -1):
                if array.size == shape[i]:
                    shape_new[i] = shape[i]
                    break
        array = array.reshape(shape_new)
    if array.ndim != len(shape):
        raise ValueError("The array has the wrong number of dimensions.")
    if array.shape[axis] == shape[axis]:
        # interpolate to staggered positions
        array_f = interp_cntr_to_stagg(array, x_f, x_c, axis)
    else:
        array_f = array
    array_f = np.broadcast_to(array_f, shape_f)
    return array_f

```
