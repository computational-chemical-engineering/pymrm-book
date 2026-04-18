# `pymrm.helpers`

## Docstring

```text
pymrm.helpers
=================

Utility helpers used throughout `pymrm`.

The functions in this module provide small building blocks that are reused in
multiple numerical routines.  They focus on preparing arrays for boundary
conditions and on constructing sparse coefficient matrices that are used in the
finite volume discretisation implemented by the package.

Functions
---------
``unwrap_bc_coeff``
    Expand boundary-condition coefficients to match an arbitrary domain shape.
``construct_coefficient_matrix``
    Create a sparse diagonal matrix from coefficient values.
``_sparse_array``
    Internal helper to construct a sparse array in the requested format.
```

