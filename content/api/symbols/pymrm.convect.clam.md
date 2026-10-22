# `pymrm.convect.clam`

[Back to module page](../modules/pymrm.convect) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`clam(normalized_c_c, normalized_x_c, normalized_x_d)`

## Summary

Compute the CLAM TVD correction in normalized-variable space.

## Documentation

CLAM, van Leer's curved-line advection method, is the parabola through
(0, 0), (x_c, x_d) and (1, 1); on a uniform grid ``c_f = 2 c_c - c_c**2``.
On a uniform grid this curve is also van Leer's harmonic limiter, and
pymrm uses the same parabola, with the same cap at ``c_f = 1``, for both:
``clam`` and ``vanleer`` agree on every stencil. Before pymrm 2.5.0
``clam`` returned the Osher curve.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/27bb54f8aa07d1b2692efefb5942380e91d4e33e/src/pymrm/convect.py#L443-L453)

```python
def clam(normalized_c_c, normalized_x_c, normalized_x_d):
    """Compute the CLAM TVD correction in normalized-variable space.

    CLAM, van Leer's curved-line advection method, is the parabola through
    (0, 0), (x_c, x_d) and (1, 1); on a uniform grid ``c_f = 2 c_c - c_c**2``.
    On a uniform grid this curve is also van Leer's harmonic limiter, and
    pymrm uses the same parabola, with the same cap at ``c_f = 1``, for both:
    ``clam`` and ``vanleer`` agree on every stencil. Before pymrm 2.5.0
    ``clam`` returned the Osher curve.
    """
    return vanleer(normalized_c_c, normalized_x_c, normalized_x_d)
```
