# `pymrm.helpers.construct_coefficient_matrix`

```python
construct_coefficient_matrix(coefficients, shape = None, axis = None, format = 'csc')
```

Build a sparse coefficient matrix with optional broadcasting and (row, col) coupling.

Modes
-----
1. shape is None
   Treat coefficients as a flat sequence placed on the diagonal of an N×N matrix.

2. shape is a single tuple, e.g. ``(Nz, Nr, ...)``
   Broadcast coefficients to that multidimensional shape (expanding leading size-1
   dimensions as needed) then place all values on the diagonal of a square matrix of
   size ``prod(shape)``. If ``axis`` is given, that dimension is first incremented
   by 1 (staggered / face-centred length) before broadcasting.

3. shape is a pair of tuples: ``(shape_rows, shape_cols)``
   A dimension in either ``shape_rows`` or ``shape_cols`` can be singular. This can
   create a (possibly rectangular) matrix that couples two fields with different
   (but same-rank) shapes. The working broadcast shape is the element-wise maximum
   of ``shape_rows`` and ``shape_cols`` (adjusted by +1 along ``axis`` if provided;
   matching staggered dims in rows/cols are expanded too).

   Result::

       n_rows = prod(shape_rows)
       n_cols = prod(shape_cols)
       nnz    = prod(working_shape)

Parameters
----------
coefficients : array_like
    Scalar field to broadcast; shape must be broadcast-compatible with the target.
shape : None | tuple | (tuple, tuple), optional
    Selects mode (see above).
axis : int, optional
    Staggered axis: length along this axis is increased by 1 for broadcasting.
format : {'csc', 'csr'}, optional
    Sparse storage format.  Default is ``'csc'``.

Returns
-------
csc_array or csr_array
    Sparse matrix in the requested format.

Notes
-----
- In mode (3) this is not a diagonal; it is a pointwise coupling pattern.
- Broadcasting follows NumPy rules after auto-prepending leading 1s.

Examples
--------
Diagonal from flat:
    A = construct_coefficient_matrix(np.ones(20))
Diagonal from 2D field (staggered in axis 0):
    A = construct_coefficient_matrix(kz, shape=(Nz, Nr), axis=0)
Rectangular coupling (cell centers -> axial faces):
    A = construct_coefficient_matrix(alpha, shape=((1, Nr), (Nz, Nr)), axis=0)
