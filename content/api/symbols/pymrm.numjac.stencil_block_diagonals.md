# `pymrm.numjac.stencil_block_diagonals`

## Signature

`pymrm.numjac.stencil_block_diagonals(ndims=1, axes_diagonals=[], axes_blocks=[-1], periodic_axes=[])`

## Docstring

```text
Generate a block-diagonal or block-banded stencil description.

Parameters
----------
ndims : int, optional
    Number of spatial dimensions.
axes_diagonals : list[int], optional
    Axes for which ``[-1, 0, 1]`` neighbor offsets are included.
axes_blocks : list[int], optional
    Axes over which full-block coupling (``slice(None)``) is applied.
periodic_axes : list[int], optional
    Axes with periodic indexing.

Returns
-------
list[tuple]
    Dependency specification in PyMRM notation.
```

## Implementation

```python
def stencil_block_diagonals(
    ndims=1, axes_diagonals=[], axes_blocks=[-1], periodic_axes=[]
):
    """Generate a block-diagonal or block-banded stencil description.

    Parameters
    ----------
    ndims : int, optional
        Number of spatial dimensions.
    axes_diagonals : list[int], optional
        Axes for which ``[-1, 0, 1]`` neighbor offsets are included.
    axes_blocks : list[int], optional
        Axes over which full-block coupling (``slice(None)``) is applied.
    periodic_axes : list[int], optional
        Axes with periodic indexing.

    Returns
    -------
    list[tuple]
        Dependency specification in PyMRM notation.
    """
    if ndims < len(axes_diagonals) or ndims < len(axes_blocks):
        raise ValueError(
            "Number of dimensions should be greater than the number of axes."
        )
    dependencies = []
    dep_block = ndims * [
        0,
    ]
    for axis in axes_blocks:
        dep_block[axis] = slice(None)
    if len(axes_diagonals) == 0:
        dep = (tuple(dep_block), tuple(dep_block), axes_blocks, periodic_axes)
        dependencies.append(dep)
    else:
        for axis in axes_diagonals:
            dep_diagonals = dep_block.copy()
            dep_diagonals[axis] = [-1, 0, 1]
            dep = (tuple(dep_diagonals), tuple(dep_block), axes_blocks, periodic_axes)
            dependencies.append(dep)
    return dependencies

```
