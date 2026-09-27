# `pymrm.numjac`

[Back to modules overview](../api)

Numerical Jacobian construction with sparse stencil support.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/numjac.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`NumJac`](../symbols/pymrm.numjac.NumJac) | class | Numerical Jacobian evaluator based on grouped finite differences. |
| [`stencil_block_diagonals`](../symbols/pymrm.numjac.stencil_block_diagonals) | function | Generate a block-diagonal or block-banded stencil description. |

## `NumJac(shape = None, shape_in = None, shape_out = None, stencil = stencil_block_diagonals, eps_jac = 1e-06, format = 'csc', **kwargs)`

[Open dedicated reference page](../symbols/pymrm.numjac.NumJac)

Numerical Jacobian evaluator based on grouped finite differences.

The class builds a sparse Jacobian structure from a stencil/dependency
description and reuses that structure across repeated evaluations.

With the default stencil every point is coupled in full along the LAST
axis and not at all along the others: right for a local term (a reaction)
on a field of shape ``(n, n_c)``. Keep a field axis for a single field,
``(n, 1)``; a bare ``(n,)`` couples all cells and builds a dense Jacobian.
Couplings between neighbouring cells normally come from the operators, not
from ``NumJac``; use ``axes_diagonals`` only when the local term itself
reads neighbours.

### Examples

>>> import numpy as np
>>> from pymrm import NumJac
>>> numjac = NumJac((5, 1))
>>> g, jac = numjac(lambda c: c**2, np.ones((5, 1)))
>>> jac.shape, jac.nnz
((5, 5), 5)

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/numjac.py#L584-L808)

## Members

### `__init__(shape = None, shape_in = None, shape_out = None, stencil = stencil_block_diagonals, eps_jac = 1e-06, format = 'csc', **kwargs)`

Create a Jacobian approximator.

#### Parameters

- `shape` (*tuple[int, ...], optional*)
  Convenience argument for square mappings where
  ``shape_in == shape_out == shape``.

- `shape_in, shape_out` (*tuple[int, ...], optional*)
  Input and output shapes for non-square mappings.

- `stencil` (*callable or list or tuple, optional*)
  Stencil specification or factory callable. When callable, it is
  invoked with ``ndims`` and ``**kwargs``.

- `eps_jac` (*float, optional*)
  Relative perturbation magnitude used in finite differences.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for produced Jacobian matrices.

- `**kwargs`
  Additional options passed to the stencil callable.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/numjac.py#L608-L675)

### `__call__(f, c, f_value = None)`

Compute the numerical Jacobian for a given function and input array.

#### Parameters

- `f` (*callable*)
  Function to evaluate. Should accept a single argument (the input array).

- `c` (*np.ndarray*)
  Input array at which to evaluate the Jacobian.

- `f_value` (*np.ndarray, optional*)
  Precomputed function value at c (i.e., f(c)). If provided, this value
  will be used directly and the function will not be called again for c.
  This is useful if f(c) has already been computed elsewhere and avoids
  redundant computation.

#### Returns

- `tuple`
  (Function value at c, Jacobian as a sparse matrix).

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/numjac.py#L760-L808)

### `init_stencil(stencil, **kwargs)`

Initialize and process the stencil (dependency pattern) for numerical Jacobian computation.

This method configures the sparsity/dependency structure used to compute numerical Jacobians,
supporting a variety of stencil specifications. The stencil can be supplied as either:

- A function (callable) that generates a dependency pattern in PyMRM dependency notation.
    The function should accept the keyword argument `ndims` (number of dimensions)
    and any additional keyword arguments.
- A pre-defined dependency specification (e.g., list or tuple) in any accepted PyMRM format,
    including full or shorthand forms.

The stencil is expanded using PyMRM's dependency notation, which allows concise or explicit
description of dependencies between positions in multidimensional fields. The result is used
to generate the internal sparsity pattern for efficient Jacobian assembly.

#### Parameters

- `stencil` (*callable or list or tuple*)
  Specification of the dependency pattern. Either a function that returns a dependency
  pattern in PyMRM notation (when called with `ndims` and additional `**kwargs`), or
  a direct specification as a list or tuple following the PyMRM dependency notation.
  See the PyMRM documentation for details on the allowed formats.

- `**kwargs`
  Additional keyword arguments passed to the stencil function (if `stencil` is callable).

#### Raises

- `ValueError`
  If no stencil is provided.

#### Side Effects

Sets the following attributes on the class:
- `self.dependencies`: Fully expanded dependency list (PyMRM notation).
- `self.rows, self.cols`: Row/column indices for the Jacobian sparsity pattern.
- `self.gr, self.num_gr`: Grouping information for column grouping.

#### References

For a full description of the PyMRM dependency notation, see:
- `dependencies_format.md` in the PyMRM package.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/numjac.py#L677-L758)

## `stencil_block_diagonals(ndims = 1, axes_diagonals = (), axes_blocks = None, periodic_axes = ())`

[Open dedicated reference page](../symbols/pymrm.numjac.stencil_block_diagonals)

Generate a block-diagonal or block-banded stencil description.

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/26b1cf19019672d855d525a0001f9d3c2a650e65/src/pymrm/numjac.py#L435-L493)
