# `pymrm.numjac`

[Back to modules overview](../api.md)

Numerical Jacobian construction with sparse stencil support.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/numjac.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`NumJac`](../symbols/pymrm.numjac.NumJac.md) | class | Numerical Jacobian evaluator based on grouped finite differences. |
| [`stencil_block_diagonals`](../symbols/pymrm.numjac.stencil_block_diagonals.md) | function | Generate a block-diagonal or block-banded stencil description. |

## `NumJac(shape = None, shape_in = None, shape_out = None, stencil = stencil_block_diagonals, eps_jac = 1e-06, format = 'csc', **kwargs)`

[Open dedicated reference page](../symbols/pymrm.numjac.NumJac.md)

Numerical Jacobian evaluator based on grouped finite differences.

The class builds a sparse Jacobian structure from a stencil/dependency
description and reuses that structure across repeated evaluations.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/numjac.py#L561-L756)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/numjac.py#L568-L623)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/numjac.py#L708-L756)

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

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/numjac.py#L625-L706)

## `stencil_block_diagonals(ndims = 1, axes_diagonals = [], axes_blocks = [-1], periodic_axes = [])`

[Open dedicated reference page](../symbols/pymrm.numjac.stencil_block_diagonals.md)

Generate a block-diagonal or block-banded stencil description.

### Parameters

- `ndims` (*int, optional*)
  Number of spatial dimensions.

- `axes_diagonals` (*list[int], optional*)
  Axes for which ``[-1, 0, 1]`` neighbor offsets are included.

- `axes_blocks` (*list[int], optional*)
  Axes over which full-block coupling (``slice(None)``) is applied.

- `periodic_axes` (*list[int], optional*)
  Axes with periodic indexing.

### Returns

- `list[tuple]`
  Dependency specification in PyMRM notation.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/numjac.py#L430-L470)
