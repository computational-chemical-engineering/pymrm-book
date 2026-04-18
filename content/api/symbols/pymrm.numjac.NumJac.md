# `pymrm.numjac.NumJac`

## Signature

`pymrm.numjac.NumJac(shape=None, shape_in=None, shape_out=None, stencil=<function stencil_block_diagonals at 0x7f50c29c6ca0>, eps_jac=1e-06, format='csc', **kwargs)`

## Docstring

```text
Numerical Jacobian evaluator based on grouped finite differences.

The class builds a sparse Jacobian structure from a stencil/dependency
description and reuses that structure across repeated evaluations.
```

## Implementation

```python
class NumJac:
    """Numerical Jacobian evaluator based on grouped finite differences.

    The class builds a sparse Jacobian structure from a stencil/dependency
    description and reuses that structure across repeated evaluations.
    """

    def __init__(
        self,
        shape=None,
        shape_in=None,
        shape_out=None,
        stencil=stencil_block_diagonals,
        eps_jac=1e-6,
        format="csc",
        **kwargs,
    ):
        """Create a Jacobian approximator.

        Parameters
        ----------
        shape : tuple[int, ...], optional
            Convenience argument for square mappings where
            ``shape_in == shape_out == shape``.
        shape_in, shape_out : tuple[int, ...], optional
            Input and output shapes for non-square mappings.
        stencil : callable or list or tuple, optional
            Stencil specification or factory callable. When callable, it is
            invoked with ``ndims`` and ``**kwargs``.
        eps_jac : float, optional
            Relative perturbation magnitude used in finite differences.
        format : {'csc', 'csr'}, optional
            Sparse format for produced Jacobian matrices.
        **kwargs
            Additional options passed to the stencil callable.
        """
        if shape is not None and (shape_in is not None or shape_out is not None):
            raise ValueError(
                "Specify either 'shape' or both 'shape_in' and 'shape_out', but not both."
            )

        if shape is not None:
            # Default case: shape_in == shape_out
            self.shape_in = shape
            self.shape_out = shape
        elif shape_in is not None and shape_out is not None:
            # General case: shape_in != shape_out
            if len(shape_in) != len(shape_out):
                raise ValueError(
                    "Input and output shapes must have the same number of dimensions."
                )
            self.shape_in = shape_in
            self.shape_out = shape_out
        else:
            raise ValueError(
                "You must specify either 'shape' or both 'shape_in' and 'shape_out'."
            )

        self.eps_jac = eps_jac
        self.format = format

        # Initialize stencil
        self.init_stencil(stencil, **kwargs)

    def init_stencil(self, stencil, **kwargs):
        """
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

        Parameters
        ----------
        stencil : callable or list or tuple
            Specification of the dependency pattern. Either a function that returns a dependency
            pattern in PyMRM notation (when called with `ndims` and additional `**kwargs`), or
            a direct specification as a list or tuple following the PyMRM dependency notation.
            See the PyMRM documentation for details on the allowed formats.
        **kwargs
            Additional keyword arguments passed to the stencil function (if `stencil` is callable).

        Raises
        ------
        ValueError
            If no stencil is provided.

        Side Effects
        ------------
        Sets the following attributes on the class:
        - `self.dependencies`: Fully expanded dependency list (PyMRM notation).
        - `self.rows, self.cols`: Row/column indices for the Jacobian sparsity pattern.
        - `self.gr, self.num_gr`: Grouping information for column grouping.

        References
        ----------
        For a full description of the PyMRM dependency notation, see:
        - `dependencies_format.md` in the PyMRM package.
        """
        if stencil is None:
            raise ValueError(
                "A stencil function or stencil specification must be provided."
            )

        # Call the stencil function with ndims, *args, and **kwargs
        if callable(stencil):
            stencil = stencil(ndims=len(self.shape_in), **kwargs)
        self.dependencies = expand_dependencies(self.shape_in, self.shape_out, stencil)
        self.rows, self.cols = generate_sparsity_pattern(
            self.shape_in, self.shape_out, self.dependencies,
            format=self.format,
        )
        self.gr, self.num_gr = colgroup(
            self.rows,
            self.cols,
            shape=(np.prod(self.shape_out), np.prod(self.shape_in)),
        )

        # Precompute compressed sparse structure so that __call__ can
        # construct the sparse matrix directly from (data, indices, indptr)
        # instead of going through the slower COO → CSR/CSC conversion.
        n_out = int(np.prod(self.shape_out))
        n_in = int(np.prod(self.shape_in))
        if self.format == "csr":
            counts = np.bincount(self.rows, minlength=n_out)
            self._indptr = np.zeros(n_out + 1, dtype=np.int64)
            np.cumsum(counts, out=self._indptr[1:])
            self._indices = self.cols.copy()
        else:
            counts = np.bincount(self.cols, minlength=n_in)
            self._indptr = np.zeros(n_in + 1, dtype=np.int64)
            np.cumsum(counts, out=self._indptr[1:])
            self._indices = self.rows.copy()

        # Precompute flat index into df.ravel() to replace 2D fancy
        # indexing with a single 1D gather in __call__.
        self._df_idx = self.gr.ravel()[self.cols] * n_out + self.rows

    def __call__(self, f, c, f_value=None):
        """
        Compute the numerical Jacobian for a given function and input array.

        Parameters
        ----------
        f : callable
            Function to evaluate. Should accept a single argument (the input array).
        c : np.ndarray
            Input array at which to evaluate the Jacobian.
        f_value : np.ndarray, optional
            Precomputed function value at c (i.e., f(c)). If provided, this value
            will be used directly and the function will not be called again for c.
            This is useful if f(c) has already been computed elsewhere and avoids
            redundant computation.

        Returns
        -------
        tuple
            (Function value at c, Jacobian as a sparse matrix).
        """
        if f_value is None:
            f_value = f(c)
        dc = -self.eps_jac * np.abs(c)
        dc[dc > (-self.eps_jac)] = self.eps_jac
        dc = (c + dc) - c

        c_perturb = np.tile(c[np.newaxis, ...], (self.num_gr,) + (1,) * c.ndim)
        c_perturb.ravel()[c.size * self.gr.ravel() + np.arange(c.size)] += dc.ravel()

        df = compute_df2(f, f_value, c_perturb, self.num_gr)

        # Compute Jacobian values using precomputed flat index
        values = df.ravel()[self._df_idx] / dc.ravel()[self.cols]

        # Construct sparse matrix directly from (data, indices, indptr),
        # bypassing the COO → compressed-format conversion.
        if self.format == "csr":
            jac = csr_array(
                (values, self._indices, self._indptr),
                shape=(f_value.size, c.size),
            )
        else:
            jac = csc_array(
                (values, self._indices, self._indptr),
                shape=(f_value.size, c.size),
            )

        return f_value, jac

```
