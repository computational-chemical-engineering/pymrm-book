# `pymrm.numjac.stencil_block_diagonals`

[Back to module page](../modules/pymrm.numjac) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`stencil_block_diagonals(ndims = 1, axes_diagonals = (), axes_blocks = None, periodic_axes = ())`

## Summary

Generate a block-diagonal or block-banded stencil description.

## Documentation

### Parameters

- `ndims` (*int, optional*)
  Number of axes of the field (spatial axes plus component axes).

- `axes_diagonals` (*sequence[int], optional*)
  Axes along which neighbour coupling (offsets ``-1, 0, 1``) is included.

- `axes_blocks` (*sequence[int] or None, optional*)
  Axes over which full-block coupling (``slice(None)``) is applied. The
  default, ``None``, means the last axis; on a 1-D field with
  ``axes_diagonals=[0]`` it means no block axes, which gives a tridiagonal
  stencil.

- `periodic_axes` (*sequence[int], optional*)
  Axes with periodic indexing.

### Returns

- `list[tuple]`
  Dependency specification in PyMRM notation.

### Notes

Axes may be given as negative numbers and are normalised modulo ``ndims``.
An axis listed both as a block and as a diagonal axis is treated as a block
axis: full coupling along it already contains the neighbour band, so the
Jacobian stays exact.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/numjac.py#L435-L493)

```python
def stencil_block_diagonals(
    ndims=1, axes_diagonals=(), axes_blocks=None, periodic_axes=()
):
    """Generate a block-diagonal or block-banded stencil description.

    Parameters
    ----------
    ndims : int, optional
        Number of axes of the field (spatial axes plus component axes).
    axes_diagonals : sequence[int], optional
        Axes along which neighbour coupling (offsets ``-1, 0, 1``) is included.
    axes_blocks : sequence[int] or None, optional
        Axes over which full-block coupling (``slice(None)``) is applied. The
        default, ``None``, means the last axis; on a 1-D field with
        ``axes_diagonals=[0]`` it means no block axes, which gives a tridiagonal
        stencil.
    periodic_axes : sequence[int], optional
        Axes with periodic indexing.

    Returns
    -------
    list[tuple]
        Dependency specification in PyMRM notation.

    Notes
    -----
    Axes may be given as negative numbers and are normalised modulo ``ndims``.
    An axis listed both as a block and as a diagonal axis is treated as a block
    axis: full coupling along it already contains the neighbour band, so the
    Jacobian stays exact.
    """

    def _normalise(axes, name):
        out = []
        for axis in axes:
            if not -ndims <= axis < ndims:
                raise ValueError(f"{name}: axis {axis} out of range for ndims={ndims}")
            out.append(axis % ndims)
        return sorted(set(out))

    diagonals = _normalise(axes_diagonals, "axes_diagonals")
    periodic = _normalise(periodic_axes, "periodic_axes")
    if axes_blocks is None:
        blocks = [] if (ndims == 1 and 0 in diagonals) else [ndims - 1]
    else:
        blocks = _normalise(axes_blocks, "axes_blocks")

    dep_block = ndims * [0]
    for axis in blocks:
        dep_block[axis] = slice(None)
    band_axes = [axis for axis in diagonals if axis not in blocks]
    if not band_axes:
        return [(tuple(dep_block), tuple(dep_block), blocks, periodic)]
    dependencies = []
    for axis in band_axes:
        dep_diagonals = dep_block.copy()
        dep_diagonals[axis] = [-1, 0, 1]
        dependencies.append((tuple(dep_diagonals), tuple(dep_block), blocks, periodic))
    return dependencies
```
