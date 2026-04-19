# `pymrm.convect.construct_convflux_upwind`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`construct_convflux_upwind(shape, x_f, x_c = None, bc = (None, None), v = 1.0, axis = 0, shapes_d = (None, None), format = 'csc')`

## Summary

Construct a first-order upwind convective-flux operator.

## Documentation

### Parameters

- `shape` (*tuple[int, ...] or int*)
  Cell-centered field shape.

- `x_f` (*array_like*)
  Face coordinates along ``axis``.

- `x_c` (*array_like, optional*)
  Cell-center coordinates. If omitted, arithmetic midpoints are used.

- `bc` (*tuple[dict | None, dict | None], optional*)
  Left and right boundary-condition dictionaries with keys ``a``, ``b``,
  and ``d``.

- `v` (*float or array_like, optional*)
  Face velocity field. Scalars and broadcastable arrays are accepted.

- `axis` (*int, optional*)
  Convection axis.

- `shapes_d` (*tuple[tuple | None, tuple | None], optional*)
  Optional source-vector shapes for boundary inhomogeneities.

- `format` (*{'csc', 'csr'}, optional*)
  Sparse format for returned operator matrices.

### Returns

- `tuple`
  Without ``shapes_d``: ``(conv_matrix, conv_bc)``.
  With ``shapes_d``: ``(conv_matrix, conv_bc_left, conv_bc_right)``.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/convect.py#L11-L69)

```python
def construct_convflux_upwind(
    shape, x_f, x_c=None, bc=(None, None), v=1.0, axis=0, shapes_d=(None, None),
    format="csc"
):
    """Construct a first-order upwind convective-flux operator.

    Parameters
    ----------
    shape : tuple[int, ...] or int
        Cell-centered field shape.
    x_f : array_like
        Face coordinates along ``axis``.
    x_c : array_like, optional
        Cell-center coordinates. If omitted, arithmetic midpoints are used.
    bc : tuple[dict | None, dict | None], optional
        Left and right boundary-condition dictionaries with keys ``a``, ``b``,
        and ``d``.
    v : float or array_like, optional
        Face velocity field. Scalars and broadcastable arrays are accepted.
    axis : int, optional
        Convection axis.
    shapes_d : tuple[tuple | None, tuple | None], optional
        Optional source-vector shapes for boundary inhomogeneities.
    format : {'csc', 'csr'}, optional
        Sparse format for returned operator matrices.

    Returns
    -------
    tuple
        Without ``shapes_d``: ``(conv_matrix, conv_bc)``.
        With ``shapes_d``: ``(conv_matrix, conv_bc_left, conv_bc_right)``.
    """
    if isinstance(shape, int):
        shape = (shape,)
    else:
        shape = tuple(shape)
    x_f, x_c = generate_grid(shape[axis], x_f, generate_x_c=True, x_c=x_c)

    v_f = create_staggered_array(v, shape, axis, x_f=x_f, x_c=x_c)
    conv_matrix = construct_convflux_upwind_int(shape, v_f, axis, format=format)
    if bc is None or bc == (None, None):
        shape_f = shape[:axis] + (shape[axis] + 1,) + shape[axis + 1:]
        conv_bc = csc_array((math.prod(shape_f), 1))
        return conv_matrix, conv_bc
    else:
        if shapes_d is None or shapes_d == (None, None):
            conv_matrix_bc, conv_bc = construct_convflux_bc(
                shape, x_f, x_c, bc, v_f, axis, format=format
            )
            conv_matrix += conv_matrix_bc
            return conv_matrix, conv_bc
        else:
            conv_matrix_bc_0, conv_bc_0, conv_matrix_bc_1, conv_bc_1 = (
                construct_convflux_bc(
                    shape, x_f, x_c, bc, v_f, axis, shapes_d=shapes_d, format=format
                )
            )
            conv_matrix += conv_matrix_bc_0 + conv_matrix_bc_1
            return conv_matrix, conv_bc_0, conv_bc_1
```
