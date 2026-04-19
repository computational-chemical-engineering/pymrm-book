# `pymrm.coupling`

[Back to modules overview](../api)

Sparse-matrix utilities for multi-domain coupling and interface assembly.

[View module source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/coupling.py)

## Public API

| Symbol | Type | Summary |
| ------ | ---- | ------- |
| [`construct_interface_matrices`](../symbols/pymrm.coupling.construct_interface_matrices) | function | Construct implicit interface-coupling matrices for two adjacent domains. |
| [`translate_indices_to_larger_array`](../symbols/pymrm.coupling.translate_indices_to_larger_array) | function | Map flat indices from a local array shape to a larger embedding shape. |
| [`update_array_indices`](../symbols/pymrm.coupling.update_array_indices) | function | Update sparse-matrix indices for a new embedding shape. |
| [`update_csc_array_indices`](../symbols/pymrm.coupling.update_csc_array_indices) | function | Update CSC matrix row/column indexing for embedding in a larger domain. |
| [`update_csr_array_indices`](../symbols/pymrm.coupling.update_csr_array_indices) | function | Update CSR matrix row/column indexing for embedding in a larger domain. |

## `construct_interface_matrices(shapes, x_fs, x_cs = (None, None), ic = ({'a': (1, 1), 'b': (0, 0), 'd': 0}, {'a': (0, 0), 'b': (1, -1), 'd': 0}), axis = 0, shapes_d = (None, None), format = 'csc')`

[Open dedicated reference page](../symbols/pymrm.coupling.construct_interface_matrices)

Construct implicit interface-coupling matrices for two adjacent domains.

### Parameters

- `shapes` (*tuple[tuple[int, ...], tuple[int, ...]]*)
  Shapes of the two subdomains.

- `x_fs` (*tuple[array_like, array_like]*)
  Face coordinates for each subdomain along ``axis``.

- `x_cs` (*tuple[array_like | None, array_like | None], optional*)
  Cell-center coordinates for each subdomain.

- `ic` (*tuple[dict, dict], optional*)
  Two interface equations. Each dictionary may define ``a``, ``b``, and
  ``d`` terms with coefficients for both subdomains.

- `axis` (*int, optional*)
  Interface-normal axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional source-vector shapes for decomposed inhomogeneous terms.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for the homogeneous interface matrices.

### Returns

- `tuple`
  Without ``shapes_d``:
  ``(mat0, bc0, mat1, bc1)``.
  With ``shapes_d``:
  ``(mat0, bc00, bc01, mat1, bc10, bc11)``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/coupling.py#L190-L394)

## `translate_indices_to_larger_array(linear_indices, shape, new_shape, offset = None)`

[Open dedicated reference page](../symbols/pymrm.coupling.translate_indices_to_larger_array)

Map flat indices from a local array shape to a larger embedding shape.

### Parameters

- `linear_indices` (*array_like*)
  Flat indices defined in ``shape``.

- `shape` (*tuple[int, ...]*)
  Local array shape.

- `new_shape` (*tuple[int, ...]*)
  Embedding array shape.

- `offset` (*tuple[int, ...], optional*)
  Offset of the local array origin in the embedding array.

### Returns

- `numpy.ndarray`
  Flat indices in ``new_shape``.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/coupling.py#L11-L43)

## `update_array_indices(sparse_mat, shape, new_shape, offset = None)`

[Open dedicated reference page](../symbols/pymrm.coupling.update_array_indices)

Update sparse-matrix indices for a new embedding shape.

### Parameters

- `sparse_mat` (*scipy.sparse.sparray*)
  Input matrix. CSR and CSC are supported.

- `shape, new_shape` (*tuple or tuple[tuple, tuple]*)
  Original and target logical shapes for rows and columns. A single tuple
  applies to both rows and columns.

- `offset` (*tuple or tuple[tuple, tuple], optional*)
  Optional row/column offsets of the local block in the larger domain.

### Returns

- `scipy.sparse.sparray`
  Matrix with updated shape and indices, preserving the input format where
  possible.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/coupling.py#L164-L187)

## `update_csc_array_indices(sparse_mat, shape, new_shape, offset = None)`

[Open dedicated reference page](../symbols/pymrm.coupling.update_csc_array_indices)

Update CSC matrix row/column indexing for embedding in a larger domain.

.. deprecated::
   Use `update_array_indices` for automatic format dispatch.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/coupling.py#L67-L78)

## `update_csr_array_indices(sparse_mat, shape, new_shape, offset = None)`

[Open dedicated reference page](../symbols/pymrm.coupling.update_csr_array_indices)

Update CSR matrix row/column indexing for embedding in a larger domain.

[View source on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/coupling.py#L123-L161)
