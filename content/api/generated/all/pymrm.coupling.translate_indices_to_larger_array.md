# `pymrm.coupling.translate_indices_to_larger_array`

```python
translate_indices_to_larger_array(linear_indices, shape, new_shape, offset = None)
```

Map flat indices from a local array shape to a larger embedding shape.

**Parameters**

- **linear_indices** : `array_like` — Flat indices defined in ``shape``.
- **shape** : `tuple[int, ...]` — Local array shape.
- **new_shape** : `tuple[int, ...]` — Embedding array shape.
- **offset** : `tuple[int, ...]` — Offset of the local array origin in the embedding array.

**Returns**

- `numpy.ndarray` — Flat indices in ``new_shape``.
