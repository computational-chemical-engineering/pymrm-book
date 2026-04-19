# `pymrm.solve.clip_approach`

[Back to module page](../modules/pymrm.solve) · [Back to alphabetical overview](../alphabetical_overview)

## Signature

`clip_approach(values, dummy, lower_bounds = 0, upper_bounds = None, factor = 0)`

## Summary

Project values onto bounds, optionally with a relaxed approach rule.

## Documentation

### Parameters

- `values` (*numpy.ndarray*)
  Values to modify in place.

- `dummy` (*Any*)
  Placeholder argument kept for API compatibility.

- `lower_bounds, upper_bounds` (*float or numpy.ndarray, optional*)
  Lower and upper bounds. Scalars and broadcastable arrays are supported.

- `factor` (*float, optional*)
  Relaxation factor for out-of-bound entries. ``0`` applies strict clipping.
  Non-zero values apply a linear approach update toward the violated bound.

## Source

[View on GitHub](https://github.com/computational-chemical-engineering/pymrm/blob/0b0ac9e5d5a7ceb669718e3aafef1ebd9960b860/src/pymrm/solve.py#L115-L146)

```python
def clip_approach(values, dummy, lower_bounds=0, upper_bounds=None, factor=0):
    """Project values onto bounds, optionally with a relaxed approach rule.

    Parameters
    ----------
    values : numpy.ndarray
        Values to modify in place.
    dummy : Any
        Placeholder argument kept for API compatibility.
    lower_bounds, upper_bounds : float or numpy.ndarray, optional
        Lower and upper bounds. Scalars and broadcastable arrays are supported.
    factor : float, optional
        Relaxation factor for out-of-bound entries. ``0`` applies strict clipping.
        Non-zero values apply a linear approach update toward the violated bound.
    """
    if factor == 0:
        np.clip(values, lower_bounds, upper_bounds, out=values)
    else:
        if lower_bounds is not None:
            below_lower = values < lower_bounds
            if np.any(below_lower):
                broadcasted_lower_bounds = np.broadcast_to(lower_bounds, values.shape)
                values[below_lower] = (1.0 + factor) * broadcasted_lower_bounds[
                    below_lower
                ] - factor * values[below_lower]
        if upper_bounds is not None:
            above_upper = values > upper_bounds
            if np.any(above_upper):
                broadcasted_upper_bounds = np.broadcast_to(upper_bounds, values.shape)
                values[above_upper] = (1.0 + factor) * broadcasted_upper_bounds[
                    above_upper
                ] - factor * values[above_upper]
```
