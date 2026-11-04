"""Template for LabVIEW-facing wrappers around an annotated Python module.

The generator replaces the placeholders below with the module import,
annotation metadata, and one wrapper per discovered function.
"""

from __future__ import annotations

import {{MODULE_NAME}}


# These dictionaries come from the source module's analyzed annotations.
TYPE_DEFINITIONS = {{TYPE_DEFINITIONS}}
FUNCTION_METADATA = {{FUNCTION_METADATA}}


def _map_nested_list(value, dimensions, converter):
    """Apply a value converter at each leaf of a nested list or tuple."""
    if dimensions == 0:
        return converter(value)

    if not isinstance(value, (list, tuple)):
        raise TypeError(
            f"Expected a {dimensions}-dimensional list of TypedDict values."
        )

    return [
        _map_nested_list(item, dimensions - 1, converter)
        for item in value
    ]


def _from_labview_value(value, parameter):
    """Convert an incoming LabVIEW value according to its analyzed annotation."""
    if parameter["container"] == "np.ndarray":
        # LabVIEW supplies arrays as Python sequences; the target function
        # expects an ndarray with the dtype declared in its annotation.
        import numpy as np

        data_type = parameter["data_type"]
        # NumPy names are stored as "np.uint8", while built-in types are
        # stored without a prefix and can be passed directly as dtype names.
        dtype = (
            getattr(np, data_type[3:])
            if data_type.startswith("np.")
            else data_type
        )
        array = np.asarray(value, dtype=dtype)
        # Reject inputs whose rank differs from the annotated array shape.
        dimensions = parameter["dimensions"]
        if array.ndim != dimensions:
            raise ValueError(
                f"NumPy parameter '{parameter['name']}' expects {dimensions} "
                f"dimensions, but received {array.ndim}."
            )
        return array

    if parameter["data_type"] != "TypedDict":
        return value

    type_definition = parameter["type_definition"]
    converter = lambda item: _typed_dict_from_labview(item, type_definition)

    if parameter["container"] == "list":
        return _map_nested_list(value, parameter["dimensions"], converter)

    return converter(value)


def _typed_dict_from_labview(value, type_definition):
    """Turn a LabVIEW cluster into a dict with its declared field names.

    LabVIEW may pass a cluster as an ordered sequence. A dict is accepted too,
    which lets callers supply fields by name.
    """
    fields = TYPE_DEFINITIONS[type_definition]

    if isinstance(value, dict):
        return {
            field["name"]: _from_labview_value(value[field["name"]], field)
            for field in fields
        }

    if not isinstance(value, (list, tuple)):
        raise TypeError(
            f"Expected LabVIEW cluster data for TypedDict '{type_definition}'."
        )

    if len(value) != len(fields):
        raise ValueError(
            f"TypedDict '{type_definition}' expects {len(fields)} fields, "
            f"but received {len(value)}."
        )

    return {
        field["name"]: _from_labview_value(field_value, field)
        for field, field_value in zip(fields, value)
    }


def _deserialize_arguments(arguments, parameters):
    """Validate the argument count and convert inputs in parameter order."""
    if len(arguments) != len(parameters):
        raise ValueError(
            f"Function expects {len(parameters)} arguments, "
            f"but received {len(arguments)}."
        )

    return tuple(
        _from_labview_value(value, parameter)
        for value, parameter in zip(arguments, parameters)
    )


def _to_labview_value(value, parameter):
    """Convert TypedDict results to clusters, including nested lists."""
    if parameter["data_type"] != "TypedDict":
        return value

    type_definition = parameter["type_definition"]
    converter = lambda item: _typed_dict_to_labview(item, type_definition)

    if parameter["container"] == "list":
        return _map_nested_list(value, parameter["dimensions"], converter)

    return converter(value)


def _typed_dict_to_labview(value, type_definition):
    """Return dict fields as a tuple in the declared LabVIEW cluster order."""
    if not isinstance(value, dict):
        raise TypeError(
            f"Expected a dictionary for TypedDict '{type_definition}'."
        )

    fields = TYPE_DEFINITIONS[type_definition]
    return tuple(
        _to_labview_value(value[field["name"]], field)
        for field in fields
    )


def _normalize_return_value(result, output_parameters):
    """Return one tuple of outputs in the order LabVIEW expects.

    A function with no declared outputs yields a single None placeholder.
    Multiple declared outputs require a tuple of matching length.
    """
    if not output_parameters:
        return (None,)

    if len(output_parameters) == 1:
        result_values = (result,)
    else:
        if not isinstance(result, tuple):
            raise TypeError(
                f"Function declares {len(output_parameters)} outputs but did not "
                "return a tuple."
            )

        if len(result) != len(output_parameters):
            raise ValueError(
                f"Function declares {len(output_parameters)} outputs but returned "
                f"{len(result)} values."
            )

        result_values = result

    return tuple(
        _to_labview_value(value, parameter)
        for value, parameter in zip(result_values, output_parameters)
    )


# The generator appends one wrapper for each analyzed source function here.
{{GENERATED_FUNCTIONS}}
