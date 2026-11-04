import argparse
import ast
import json
from os import PathLike

ParameterMetadata = dict[str, object]
TypedDictMetadata = dict[str, list[ParameterMetadata]]

SUPPORTED_DATA_TYPES = {
    "int",
    "float",
    "bool",
    "str",
    "TypedDict",
    "np.bool_",
    "np.int8",
    "np.int16",
    "np.int32",
    "np.int64",
    "np.uint8",
    "np.uint16",
    "np.uint32",
    "np.uint64",
    "np.float32",
    "np.float64",
    "np.str_",
}
SUPPORTED_LIST_CONTAINERS = {"list", "List", "typing.List"}
SUPPORTED_NUMPY_CONTAINERS = {"np.ndarray"}
UNSUPPORTED_DICT_CONTAINERS = {"dict", "Dict", "typing.Dict"}
SUPPORTED_TUPLE_CONTAINERS = {"tuple"}
KNOWN_PARAMETERIZED_CONTAINERS = (
    SUPPORTED_LIST_CONTAINERS
    | SUPPORTED_NUMPY_CONTAINERS
    | UNSUPPORTED_DICT_CONTAINERS
    | SUPPORTED_TUPLE_CONTAINERS
)


def _metadata_entry(
    name: str,
    data_type: str,
    container: str = "",
    dimensions: int = 0,
    type_definition: str = "",
    *,
    typed_dicts: TypedDictMetadata,
) -> ParameterMetadata:
    """Create the uniform metadata shape used for every parameter-like item.

    Args:
        name: Parameter or field name.
        data_type: Scalar or element type, such as ``int``, ``np.float64``,
            or ``TypedDict``.
        container: Container type. Empty string means scalar/non-container.
            Currently supported container values are ``list`` and
            ``np.ndarray``.
        dimensions: Number of dimensions for containers. Scalars use 0.
        type_definition: Referenced TypedDict name. Empty string means no
            external type definition is required.
        typed_dicts: Collected TypedDict definitions used to validate references.

    Returns:
        A dictionary that can be serialized directly into JSON.
    """
    if data_type not in SUPPORTED_DATA_TYPES:
        raise ValueError(f"Unsupported data type for '{name}': {data_type}.")
    if data_type == "TypedDict" and type_definition not in typed_dicts:
        raise ValueError(
            f"TypedDict annotation for '{name}' must reference a defined "
            f"TypedDict class; got {type_definition!r}."
        )

    return {
        "name": name,
        "data_type": data_type,
        "container": container,
        "dimensions": dimensions,
        "type_definition": type_definition,
    }


def _get_numpy_array_metadata(annotation: ast.expr) -> dict[str, int | str] | None:
    """Return metadata for supported NumPy array annotations.

    Supported annotations have this form:

        np.ndarray[tuple[int, int], np.dtype[np.float64]]

    The tuple length determines the array rank/dimensions. The dtype argument
    becomes ``data_type``. The array class itself becomes ``container``.

    Args:
        annotation: AST node for a parameter or return annotation.

    Returns:
        Parsed annotation metadata when the annotation is a supported NumPy
        array. The caller adds the parameter or field name. Returns ``None``
        for other annotations.
    """
    if ast.unparse(annotation) == "np.ndarray":
        raise ValueError(
            "NumPy array annotation must specify a shape containing int "
            "dimensions (for example, tuple[int, int]) and a dtype."
        )

    if not isinstance(annotation, ast.Subscript):
        return None

    if ast.unparse(annotation.value) not in SUPPORTED_NUMPY_CONTAINERS:
        return None

    if not isinstance(annotation.slice, ast.Tuple) or len(annotation.slice.elts) != 2:
        raise ValueError(
            "NumPy array annotation must specify a shape containing int "
            "dimensions (for example, tuple[int, int]) and a dtype."
        )

    shape_annotation, dtype_annotation = annotation.slice.elts

    if not (
        isinstance(shape_annotation, ast.Subscript)
        and ast.unparse(shape_annotation.value) == "tuple"
    ):
        raise ValueError(
            "NumPy array shape must be a tuple containing only int dimensions."
        )

    shape_dimensions = (
        shape_annotation.slice.elts
        if isinstance(shape_annotation.slice, ast.Tuple)
        else [shape_annotation.slice]
    )
    if not shape_dimensions or any(
        not isinstance(dimension, ast.Name) or dimension.id != "int"
        for dimension in shape_dimensions
    ):
        raise ValueError(
            "NumPy array shape must be a tuple containing only int dimensions."
        )
    dimensions = len(shape_dimensions)

    data_type = ast.unparse(dtype_annotation)
    if (
        isinstance(dtype_annotation, ast.Subscript)
        and ast.unparse(dtype_annotation.value) == "np.dtype"
    ):
        data_type = ast.unparse(dtype_annotation.slice)

    return {
        "data_type": data_type,
        "container": ast.unparse(annotation.value),
        "dimensions": dimensions,
        "type_definition": "",
    }


def _is_typed_dict_class(node: ast.ClassDef) -> bool:
    """Return whether a class definition inherits from TypedDict."""
    return any(
        ast.unparse(base) in {"TypedDict", "typing.TypedDict"} for base in node.bases
    )


def _is_dict_annotation(annotation: ast.expr) -> bool:
    """Return whether an annotation is a plain or parameterized dict.

    Plain dictionaries are intentionally unsupported because LabVIEW cannot
    generate a strict cluster without knowing the fixed field names and types.
    Users must use TypedDict for dictionary-like values.
    """
    if isinstance(annotation, ast.Subscript):
        annotation = annotation.value

    return ast.unparse(annotation) in UNSUPPORTED_DICT_CONTAINERS


def _is_list_annotation(annotation: ast.expr) -> bool:
    """Return whether an annotation is a plain or parameterized list."""
    if isinstance(annotation, ast.Subscript):
        annotation = annotation.value

    return ast.unparse(annotation) in SUPPORTED_LIST_CONTAINERS


def _raise_for_unsupported_container(name: str, annotation: ast.expr) -> None:
    """Raise a clear error for unsupported parameterized containers."""
    if not isinstance(annotation, ast.Subscript):
        return

    container = ast.unparse(annotation.value)
    if container in KNOWN_PARAMETERIZED_CONTAINERS:
        return

    raise ValueError(
        f"Unsupported container for '{name}': {container}. "
        "Supported containers are list and np.ndarray."
    )


def _raise_for_unsupported_data_type(
    name: str,
    data_type: str,
    description: str = "data type",
) -> None:
    """Raise if a scalar or container element data type is unsupported."""
    if data_type in SUPPORTED_DATA_TYPES:
        return

    raise ValueError(f"Unsupported {description} for '{name}': {data_type}.")


def _get_list_metadata(
    annotation: ast.expr,
    typed_dicts: TypedDictMetadata,
) -> ParameterMetadata | None:
    """Return metadata for supported Python list annotations.

    Lists are represented as a container plus an element ``data_type``. Nested
    lists increase ``dimensions``:

        list[int] -> container=list, data_type=int, dimensions=1
        list[list[int]] -> container=list, data_type=int, dimensions=2

    Lists of TypedDicts are supported and reference the matching top-level
    type definition. Lists of plain dicts are rejected for the same reason as
    plain dict parameters.

    Args:
        annotation: AST node for a parameter or return annotation.
        typed_dicts: Mapping of TypedDict names to their parsed fields.

    Returns:
        Parsed annotation metadata when the annotation is a supported list.
        The caller adds the parameter or field name. Returns ``None`` for
        other annotations.

    Raises:
        ValueError: If the list element type is a plain dict annotation.
    """
    if not isinstance(annotation, ast.Subscript):
        return None

    if not _is_list_annotation(annotation):
        return None

    dimensions = 1
    element_annotation = annotation.slice

    while isinstance(element_annotation, ast.Subscript) and _is_list_annotation(
        element_annotation
    ):
        dimensions += 1
        element_annotation = element_annotation.slice

    element_type = ast.unparse(element_annotation)

    if element_type in typed_dicts:
        return {
            "data_type": "TypedDict",
            "container": "list",
            "dimensions": dimensions,
            "type_definition": element_type,
        }

    if _is_dict_annotation(element_annotation):
        raise ValueError(
            "Unsupported dictionary list annotation: "
            f"{ast.unparse(annotation)}. Use a TypedDict class instead."
        )

    _raise_for_unsupported_data_type(
        ast.unparse(annotation),
        element_type,
        "list element type",
    )

    return {
        "data_type": element_type,
        "container": "list",
        "dimensions": dimensions,
        "type_definition": "",
    }


def _collect_typed_dicts(tree: ast.Module) -> TypedDictMetadata:
    """Collect top-level TypedDict definitions from the parsed module.

    The analyzer exposes TypedDict classes as flat type definitions. Function
    parameters and fields reference them by name through ``type_definition``.
    This avoids recursive JSON structures that are difficult to model as
    LabVIEW typedef clusters.

    Args:
        tree: Parsed AST for the source file.

    Returns:
        Mapping from TypedDict class name to its field metadata.
    """
    typed_dict_nodes = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and _is_typed_dict_class(node)
    }
    typed_dicts: TypedDictMetadata = {
        typed_dict_name: [] for typed_dict_name in typed_dict_nodes
    }

    for typed_dict_name, typed_dict_node in typed_dict_nodes.items():
        fields = []

        for statement in typed_dict_node.body:
            if not (
                isinstance(statement, ast.AnnAssign)
                and isinstance(statement.target, ast.Name)
            ):
                continue

            fields.append(
                _parameter_metadata(
                    statement.target.id,
                    statement.annotation,
                    typed_dicts,
                )
            )

        # Fill the entry created in the first pass. Registering all TypedDict names
        # up front lets fields refer to classes declared later in the module.
        typed_dicts[typed_dict_name].extend(fields)

    return typed_dicts


def _typed_dict_dependencies(fields: list[ParameterMetadata]) -> set[str]:
    """Return the type definitions referenced by a TypedDict's fields."""
    dependencies = set()

    for field in fields:
        if field["data_type"] == "TypedDict" and field["type_definition"] != "":
            dependencies.add(str(field["type_definition"]))

    return dependencies


def _sort_typed_dicts_by_dependency(
    typed_dicts: TypedDictMetadata,
) -> list[tuple[str, list[ParameterMetadata]]]:
    """Sort TypedDict definitions so referenced types appear first.

    LabVIEW creates typedefs sequentially. If one typedef contains a field
    that references another typedef, the referenced typedef must already
    exist. This topological sort makes the JSON order usable directly by
    LabVIEW, even for multi-level nested TypedDict chains.

    Args:
        typed_dicts: Mapping from TypedDict class name to parsed fields.

    Returns:
        TypedDict items ordered so dependencies come before dependents.

    Raises:
        ValueError: If dependencies contain a cycle or reference a missing
            type definition.
    """
    ordered = []
    resolved = set()
    unresolved = list(typed_dicts)

    while unresolved:
        next_unresolved = []
        progress = False

        for name in unresolved:
            dependencies = _typed_dict_dependencies(typed_dicts[name])
            missing_dependencies = dependencies - set(typed_dicts)

            if missing_dependencies:
                missing = ", ".join(sorted(missing_dependencies))
                raise ValueError(
                    f"TypedDict '{name}' references unknown type definition(s): "
                    f"{missing}."
                )

            if dependencies <= resolved:
                ordered.append((name, typed_dicts[name]))
                resolved.add(name)
                progress = True
            else:
                next_unresolved.append(name)

        if not progress:
            remaining = ", ".join(next_unresolved)
            raise ValueError(
                "TypedDict definitions contain a dependency cycle: " f"{remaining}."
            )

        unresolved = next_unresolved

    return ordered


def _parameter_metadata(
    name: str,
    annotation: ast.expr | None,
    typed_dicts: TypedDictMetadata,
) -> ParameterMetadata:
    """Convert one annotation into the analyzer's uniform metadata schema.

    The conversion order matters:
    1. NumPy arrays need special parsing to extract rank and dtype.
    2. Lists need special parsing to count nested dimensions.
    3. TypedDict names become references to flat type definitions.
    4. Plain dictionaries are rejected.
    5. Supported scalar annotations are accepted.
    6. Everything else raises an error.

    Args:
        name: Parameter or field name.
        annotation: AST annotation node. Missing annotations are invalid.
        typed_dicts: Mapping of known TypedDict names to their parsed fields.

    Returns:
        Parameter metadata with keys ``name``, ``data_type``, ``container``,
        ``dimensions``, and ``type_definition``.

    Raises:
        ValueError: If the annotation is missing or uses unsupported dict
            syntax.
    """
    if annotation is None:
        raise ValueError(f"Missing type annotation for parameter '{name}'.")

    annotation_name = ast.unparse(annotation)

    numpy_array_metadata = _get_numpy_array_metadata(annotation)
    if numpy_array_metadata:
        _raise_for_unsupported_data_type(
            name,
            str(numpy_array_metadata["data_type"]),
            "NumPy dtype",
        )
        return _metadata_entry(name, **numpy_array_metadata, typed_dicts=typed_dicts)

    list_metadata = _get_list_metadata(annotation, typed_dicts)
    if list_metadata:
        return _metadata_entry(name, **list_metadata, typed_dicts=typed_dicts)

    if annotation_name in typed_dicts:
        return _metadata_entry(
            name, "TypedDict", type_definition=annotation_name, typed_dicts=typed_dicts
        )

    if _is_dict_annotation(annotation):
        raise ValueError(
            f"Unsupported dictionary annotation for '{name}': "
            f"{annotation_name}. Use a TypedDict class instead."
        )

    _raise_for_unsupported_container(name, annotation)
    _raise_for_unsupported_data_type(name, annotation_name)

    return _metadata_entry(name, annotation_name, typed_dicts=typed_dicts)


def analyze_script(path: str | PathLike[str]) -> str:
    """Return JSON metadata for top-level functions in a Python source file.

    Parses the Python file at ``path`` and returns a JSON string containing
    flat type definitions plus each top-level function's name, docstring,
    input parameter annotations, and output parameter annotations.

    The returned JSON has this top-level shape:

        {
          "type_definitions": [...],
          "functions": [...]
        }

    ``type_definitions`` contains the TypedDict classes first, followed by
    input and output parameter definitions for each function. Generated
    definition names use title case with spaces between words. Function
    inputs/outputs and TypedDict fields reference TypedDict definitions by name.

    Args:
        path: Path to the Python source file to analyze.

    Returns:
        A JSON string with discovered function metadata.
    """
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    typed_dicts = _collect_typed_dicts(tree)
    functions = []

    for node in tree.body:

        if isinstance(node, ast.FunctionDef):

            if node.args.posonlyargs:
                raise ValueError(
                    f"Function '{node.name}' has positional-only parameters; "
                    "only ordinary parameters are supported."
                )
            if node.args.kwonlyargs:
                raise ValueError(
                    f"Function '{node.name}' has keyword-only parameters; "
                    "only ordinary parameters are supported."
                )
            if node.args.vararg is not None:
                raise ValueError(
                    f"Function '{node.name}' has *args; "
                    "only ordinary parameters are supported."
                )
            if node.args.kwarg is not None:
                raise ValueError(
                    f"Function '{node.name}' has **kwargs; "
                    "only ordinary parameters are supported."
                )

            docstring = ast.get_docstring(node)
            input_parameters = []

            for arg in node.args.args:

                input_parameters.append(
                    _parameter_metadata(arg.arg, arg.annotation, typed_dicts)
                )

            if not input_parameters:
                raise ValueError(
                    f"Function '{node.name}' must have at least one input parameter."
                )

            output_parameters = []
            if node.returns and ast.unparse(node.returns) != "None":
                if isinstance(node.returns, ast.Subscript) and (
                    ast.unparse(node.returns.value) == "tuple"
                ):
                    if (
                        not isinstance(node.returns.slice, ast.Tuple)
                        or not node.returns.slice.elts
                    ):
                        raise ValueError(
                            f"Function '{node.name}' has a malformed tuple return "
                            "annotation; use tuple[T1, T2, ...]."
                        )
                    return_types = node.returns.slice.elts
                else:
                    return_types = [node.returns]

                for index, return_type in enumerate(return_types):
                    output_parameters.append(
                        _parameter_metadata(f"return_{index}", return_type, typed_dicts)
                    )

            if not output_parameters:
                raise ValueError(
                    f"Function '{node.name}' must have at least one output parameter."
                )

            functions.append(
                {
                    "name": node.name,
                    "docstring": docstring,
                    "input_parameters": input_parameters,
                    "output_parameters": output_parameters,
                }
            )

    type_definitions = [
        {
            "name": name,
            "fields": fields,
        }
        for name, fields in _sort_typed_dicts_by_dependency(typed_dicts)
    ]

    for function in functions:
        for direction in ("input", "output"):
            fields = function[f"{direction}_parameters"]
            if not fields:
                continue

            name = f"{function['name']}_{direction}_parameters"
            type_definitions.append(
                {
                    "name": name.replace("_", " ").replace("-", " ").title(),
                    "fields": fields,
                }
            )

    return json.dumps(
        {
            "type_definitions": type_definitions,
            "functions": functions,
        },
        indent=2,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze top-level functions in a Python source file."
    )
    parser.add_argument(
        "path",
        help="Path to the Python source file to analyze.",
    )
    args = parser.parse_args()

    print(analyze_script(args.path))
