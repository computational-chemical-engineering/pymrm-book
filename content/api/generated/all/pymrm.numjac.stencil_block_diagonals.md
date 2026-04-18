# `pymrm.numjac.stencil_block_diagonals`

```python
stencil_block_diagonals(ndims = 1, axes_diagonals = [], axes_blocks = [-1], periodic_axes = [])
```

Generate a block-diagonal or block-banded stencil description.

**Parameters**

- **ndims** : `int` — Number of spatial dimensions.
- **axes_diagonals** : `list[int]` — Axes for which ``[-1, 0, 1]`` neighbor offsets are included.
- **axes_blocks** : `list[int]` — Axes over which full-block coupling (``slice(None)``) is applied.
- **periodic_axes** : `list[int]` — Axes with periodic indexing.

**Returns**

- `list[tuple]` — Dependency specification in PyMRM notation.
