# `pymrm.numjac.NumJac`

```python
NumJac(self, shape = None, shape_in = None, shape_out = None, stencil = stencil_block_diagonals, eps_jac = 1e-06, format = 'csc', kwargs = {})
```

Create a Jacobian approximator.

**Parameters**

- **shape** : `tuple[int, ...]` — Convenience argument for square mappings where
``shape_in == shape_out == shape``.
- **shape_in** : `tuple[int, ...]` — Input and output shapes for non-square mappings.
- **shape_out** : `tuple[int, ...]` — Input and output shapes for non-square mappings.
- **stencil** : `callable or list or tuple` — Stencil specification or factory callable. When callable, it is
invoked with ``ndims`` and ``**kwargs``.
- **eps_jac** : `float` — Relative perturbation magnitude used in finite differences.
- **format** : `(csc, csr)` — Sparse format for produced Jacobian matrices.
- ****kwargs** — Additional options passed to the stencil callable.

## Methods

### `init_stencil`

```python
init_stencil(self, stencil, kwargs = {})
```

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

**Parameters**

- **stencil** : `callable or list or tuple` — Specification of the dependency pattern. Either a function that returns a dependency
pattern in PyMRM notation (when called with `ndims` and additional `**kwargs`), or
a direct specification as a list or tuple following the PyMRM dependency notation.
See the PyMRM documentation for details on the allowed formats.
- ****kwargs** — Additional keyword arguments passed to the stencil function (if `stencil` is callable).

**Raises**

- **ValueError** — If no stencil is provided.
