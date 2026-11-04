import json
from pathlib import Path

import pytest

from analyze import analyze_script

PARAMETER_KEYS = {
    "name",
    "data_type",
    "container",
    "dimensions",
    "type_definition",
}


def assert_parameter_schema_is_uniform(parameter):
    assert set(parameter) == PARAMETER_KEYS


def assert_type_definition_schema_is_flat(type_definition):
    assert set(type_definition) == {"name", "fields"}

    for field in type_definition["fields"]:
        assert_parameter_schema_is_uniform(field)


def test_analyze_script_reports_top_level_function_metadata(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        '''
def add(left: int, right: float = 1.0) -> float:
    """Add two numbers."""
    return left + right


def greet(name: str) -> str:
    return f"Hello {name}"
''',
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata == {
        "type_definitions": [
            {
                "name": "Add Input Parameters",
                "fields": metadata["functions"][0]["input_parameters"],
            },
            {
                "name": "Add Output Parameters",
                "fields": metadata["functions"][0]["output_parameters"],
            },
            {
                "name": "Greet Input Parameters",
                "fields": metadata["functions"][1]["input_parameters"],
            },
            {
                "name": "Greet Output Parameters",
                "fields": metadata["functions"][1]["output_parameters"],
            },
        ],
        "functions": [
            {
                "name": "add",
                "docstring": "Add two numbers.",
                "input_parameters": [
                    {
                        "name": "left",
                        "data_type": "int",
                        "container": "",
                        "dimensions": 0,
                        "type_definition": "",
                    },
                    {
                        "name": "right",
                        "data_type": "float",
                        "container": "",
                        "dimensions": 0,
                        "type_definition": "",
                    },
                ],
                "output_parameters": [
                    {
                        "name": "return_0",
                        "data_type": "float",
                        "container": "",
                        "dimensions": 0,
                        "type_definition": "",
                    }
                ],
            },
            {
                "name": "greet",
                "docstring": None,
                "input_parameters": [
                    {
                        "name": "name",
                        "data_type": "str",
                        "container": "",
                        "dimensions": 0,
                        "type_definition": "",
                    }
                ],
                "output_parameters": [
                    {
                        "name": "return_0",
                        "data_type": "str",
                        "container": "",
                        "dimensions": 0,
                        "type_definition": "",
                    }
                ],
            },
        ],
    }


def test_analyze_script_reports_tuple_return_types_as_multiple_outputs(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def split_value(value: int) -> tuple[int, float]:
    return value, float(value)
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata["functions"][0]["output_parameters"] == [
        {
            "name": "return_0",
            "data_type": "int",
            "container": "",
            "dimensions": 0,
            "type_definition": "",
        },
        {
            "name": "return_1",
            "data_type": "float",
            "container": "",
            "dimensions": 0,
            "type_definition": "",
        },
    ]


@pytest.mark.parametrize("return_annotation", ["tuple[int]", "tuple[()]"])
def test_analyze_script_rejects_malformed_tuple_returns(tmp_path, return_annotation):
    source = tmp_path / "sample.py"
    source.write_text(
        f"def process(value: int) -> {return_annotation}:\n    return value\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="malformed tuple return annotation"):
        analyze_script(source)


def test_analyze_script_reports_numpy_scalar_dtypes(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
import numpy as np


def scale_value(value: np.float32, factor: np.float32) -> np.float32:
    return value * factor
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata["functions"][0]["input_parameters"] == [
        {
            "name": "value",
            "data_type": "np.float32",
            "container": "",
            "dimensions": 0,
            "type_definition": "",
        },
        {
            "name": "factor",
            "data_type": "np.float32",
            "container": "",
            "dimensions": 0,
            "type_definition": "",
        },
    ]
    assert metadata["functions"][0]["output_parameters"] == [
        {
            "name": "return_0",
            "data_type": "np.float32",
            "container": "",
            "dimensions": 0,
            "type_definition": "",
        }
    ]


@pytest.mark.parametrize(
    "function_source",
    [
        "def log_message(message: str) -> None:\n    print(message)\n",
        "def log_message(message: str):\n    print(message)\n",
    ],
)
def test_analyze_script_rejects_functions_without_outputs(tmp_path, function_source):
    source = tmp_path / "sample.py"
    source.write_text(function_source, encoding="utf-8")

    with pytest.raises(ValueError, match="at least one output parameter"):
        analyze_script(source)


@pytest.mark.parametrize(
    "function_source,function_name",
    [
        ("def get_value() -> int:\n    return 1\n", "get_value"),
        ("def do_nothing() -> None:\n    pass\n", "do_nothing"),
    ],
)
def test_analyze_script_rejects_functions_without_inputs(
    tmp_path, function_source, function_name
):
    source = tmp_path / "sample.py"
    source.write_text(function_source, encoding="utf-8")

    with pytest.raises(
        ValueError, match=f"Function '{function_name}'.*at least one input"
    ):
        analyze_script(source)


@pytest.mark.parametrize(
    "parameters,error_message",
    [
        ("value: int, /", "positional-only parameters"),
        ("value: int, *, extra: int", "keyword-only parameters"),
        ("value: int, *args: int", r"\*args"),
        ("value: int, **kwargs: int", r"\*\*kwargs"),
    ],
)
def test_analyze_script_rejects_nonordinary_parameters(
    tmp_path, parameters, error_message
):
    source = tmp_path / "sample.py"
    source.write_text(
        f"def process({parameters}) -> int:\n    return value\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=error_message):
        analyze_script(source)


def test_analyze_script_reports_numpy_array_dimensions_and_dtype(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
import numpy as np


def factor_numpy_array(
    array_in: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    factor: float,
) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
    return array_in * factor
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata["functions"][0]["input_parameters"] == [
        {
            "name": "array_in",
            "data_type": "np.float64",
            "container": "np.ndarray",
            "dimensions": 2,
            "type_definition": "",
        },
        {
            "name": "factor",
            "data_type": "float",
            "container": "",
            "dimensions": 0,
            "type_definition": "",
        },
    ]
    assert metadata["functions"][0]["output_parameters"] == [
        {
            "name": "return_0",
            "data_type": "np.float64",
            "container": "np.ndarray",
            "dimensions": 2,
            "type_definition": "",
        }
    ]


def test_analyze_script_reports_numpy_array_ranks_and_dtypes(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
import numpy as np


def arrays(
    integers: np.ndarray[tuple[int], np.dtype[np.int64]],
    booleans: np.ndarray[tuple[int, int, int], np.dtype[np.bool_]],
    strings: np.ndarray[tuple[int], np.dtype[np.str_]],
) -> tuple[
    np.ndarray[tuple[int], np.dtype[np.int64]],
    np.ndarray[tuple[int, int, int], np.dtype[np.bool_]],
    np.ndarray[tuple[int], np.dtype[np.str_]],
]:
    return integers, booleans, strings
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata["functions"][0]["input_parameters"] == [
        {
            "name": "integers",
            "data_type": "np.int64",
            "container": "np.ndarray",
            "dimensions": 1,
            "type_definition": "",
        },
        {
            "name": "booleans",
            "data_type": "np.bool_",
            "container": "np.ndarray",
            "dimensions": 3,
            "type_definition": "",
        },
        {
            "name": "strings",
            "data_type": "np.str_",
            "container": "np.ndarray",
            "dimensions": 1,
            "type_definition": "",
        },
    ]
    assert metadata["functions"][0]["output_parameters"] == [
        {
            "name": "return_0",
            "data_type": "np.int64",
            "container": "np.ndarray",
            "dimensions": 1,
            "type_definition": "",
        },
        {
            "name": "return_1",
            "data_type": "np.bool_",
            "container": "np.ndarray",
            "dimensions": 3,
            "type_definition": "",
        },
        {
            "name": "return_2",
            "data_type": "np.str_",
            "container": "np.ndarray",
            "dimensions": 1,
            "type_definition": "",
        },
    ]


def test_analyze_script_reports_list_dimensions_and_dtypes(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def lists(
    integers: list[int],
    booleans: list[list[bool]],
    strings: list[str],
) -> tuple[
    list[int],
    list[list[bool]],
    list[str],
]:
    return integers, booleans, strings
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata["functions"][0]["input_parameters"] == [
        {
            "name": "integers",
            "data_type": "int",
            "container": "list",
            "dimensions": 1,
            "type_definition": "",
        },
        {
            "name": "booleans",
            "data_type": "bool",
            "container": "list",
            "dimensions": 2,
            "type_definition": "",
        },
        {
            "name": "strings",
            "data_type": "str",
            "container": "list",
            "dimensions": 1,
            "type_definition": "",
        },
    ]
    assert metadata["functions"][0]["output_parameters"] == [
        {
            "name": "return_0",
            "data_type": "int",
            "container": "list",
            "dimensions": 1,
            "type_definition": "",
        },
        {
            "name": "return_1",
            "data_type": "bool",
            "container": "list",
            "dimensions": 2,
            "type_definition": "",
        },
        {
            "name": "return_2",
            "data_type": "str",
            "container": "list",
            "dimensions": 1,
            "type_definition": "",
        },
    ]


def test_analyze_script_reports_flat_type_definitions_for_typed_dicts(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
from typing import TypedDict


class Config(TypedDict):
    retries: int
    enabled: bool


class Result(TypedDict):
    status: str
    value: float


def process_config(config: Config) -> Result:
    return {"status": "ok", "value": float(config["retries"])}
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata["type_definitions"] == [
        {
            "name": "Config",
            "fields": [
                {
                    "name": "retries",
                    "data_type": "int",
                    "container": "",
                    "dimensions": 0,
                    "type_definition": "",
                },
                {
                    "name": "enabled",
                    "data_type": "bool",
                    "container": "",
                    "dimensions": 0,
                    "type_definition": "",
                },
            ],
        },
        {
            "name": "Result",
            "fields": [
                {
                    "name": "status",
                    "data_type": "str",
                    "container": "",
                    "dimensions": 0,
                    "type_definition": "",
                },
                {
                    "name": "value",
                    "data_type": "float",
                    "container": "",
                    "dimensions": 0,
                    "type_definition": "",
                },
            ],
        },
        {
            "name": "Process Config Input Parameters",
            "fields": metadata["functions"][0]["input_parameters"],
        },
        {
            "name": "Process Config Output Parameters",
            "fields": metadata["functions"][0]["output_parameters"],
        },
    ]
    assert metadata["functions"][0]["input_parameters"] == [
        {
            "name": "config",
            "data_type": "TypedDict",
            "container": "",
            "dimensions": 0,
            "type_definition": "Config",
        }
    ]
    assert metadata["functions"][0]["output_parameters"] == [
        {
            "name": "return_0",
            "data_type": "TypedDict",
            "container": "",
            "dimensions": 0,
            "type_definition": "Result",
        }
    ]


def test_analyze_script_reports_typed_dict_fields_with_numpy_arrays(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
from typing import TypedDict

import numpy as np


class ArrayConfig(TypedDict):
    values: np.ndarray[tuple[int, int], np.dtype[np.float64]]
    enabled: bool


def process_array_config(config: ArrayConfig) -> ArrayConfig:
    return config
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata["type_definitions"][0]["fields"] == [
        {
            "name": "values",
            "data_type": "np.float64",
            "container": "np.ndarray",
            "dimensions": 2,
            "type_definition": "",
        },
        {
            "name": "enabled",
            "data_type": "bool",
            "container": "",
            "dimensions": 0,
            "type_definition": "",
        },
    ]


def test_analyze_script_reports_nested_typed_dicts_as_type_definition_references(
    tmp_path,
):
    source = tmp_path / "sample.py"
    source.write_text(
        """
from typing import TypedDict


class Config(TypedDict):
    calibration: Calibration
    label: str


class Calibration(TypedDict):
    gain: float
    offset: float


def process_config(config: Config) -> Config:
    return config
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata["type_definitions"] == [
        {
            "name": "Calibration",
            "fields": [
                {
                    "name": "gain",
                    "data_type": "float",
                    "container": "",
                    "dimensions": 0,
                    "type_definition": "",
                },
                {
                    "name": "offset",
                    "data_type": "float",
                    "container": "",
                    "dimensions": 0,
                    "type_definition": "",
                },
            ],
        },
        {
            "name": "Config",
            "fields": [
                {
                    "name": "calibration",
                    "data_type": "TypedDict",
                    "container": "",
                    "dimensions": 0,
                    "type_definition": "Calibration",
                },
                {
                    "name": "label",
                    "data_type": "str",
                    "container": "",
                    "dimensions": 0,
                    "type_definition": "",
                },
            ],
        },
        {
            "name": "Process Config Input Parameters",
            "fields": metadata["functions"][0]["input_parameters"],
        },
        {
            "name": "Process Config Output Parameters",
            "fields": metadata["functions"][0]["output_parameters"],
        },
    ]


def test_analyze_script_orders_type_definitions_by_dependency(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
from typing import TypedDict


class ExperimentConfig(TypedDict):
    acquisition: AcquisitionConfig
    operator: str


class AcquisitionConfig(TypedDict):
    sensor: SensorConfig
    sample_rate: float


class SensorConfig(TypedDict):
    calibration: SensorCalibration
    serial_number: str


class SensorCalibration(TypedDict):
    gain: float
    offset: float


def process_config(config: ExperimentConfig) -> ExperimentConfig:
    return config
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert [definition["name"] for definition in metadata["type_definitions"]] == [
        "SensorCalibration",
        "SensorConfig",
        "AcquisitionConfig",
        "ExperimentConfig",
        "Process Config Input Parameters",
        "Process Config Output Parameters",
    ]


def test_analyze_script_rejects_typed_dict_dependency_cycles(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
from typing import TypedDict


class First(TypedDict):
    second: Second


class Second(TypedDict):
    first: First


def process_config(config: First) -> First:
    return config
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="dependency cycle"):
        analyze_script(source)


def test_analyze_script_reports_uniform_flat_schema_for_dummy_module():
    metadata = json.loads(analyze_script(Path(__file__).with_name("dummy_module.py")))

    assert set(metadata) == {"type_definitions", "functions"}

    for type_definition in metadata["type_definitions"]:
        assert_type_definition_schema_is_flat(type_definition)

    for function in metadata["functions"]:
        for parameter in function["input_parameters"]:
            assert_parameter_schema_is_uniform(parameter)

        for parameter in function["output_parameters"]:
            assert_parameter_schema_is_uniform(parameter)


def test_analyze_script_reports_typed_dict_list_type_definition_references(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
from typing import TypedDict


class Measurement(TypedDict):
    value: float
    valid: bool


def process_measurements(
    measurements: list[Measurement],
) -> list[list[Measurement]]:
    return [measurements]
""",
        encoding="utf-8",
    )

    metadata = json.loads(analyze_script(source))

    assert metadata["functions"][0]["input_parameters"] == [
        {
            "name": "measurements",
            "data_type": "TypedDict",
            "container": "list",
            "dimensions": 1,
            "type_definition": "Measurement",
        }
    ]
    assert metadata["functions"][0]["output_parameters"] == [
        {
            "name": "return_0",
            "data_type": "TypedDict",
            "container": "list",
            "dimensions": 2,
            "type_definition": "Measurement",
        }
    ]


def test_analyze_script_rejects_unsupported_dict_input_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def process_config(config: dict[str, int]) -> int:
    return config
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Use a TypedDict class"):
        analyze_script(source)


@pytest.mark.parametrize("annotation", ["TypedDict", "list[TypedDict]"])
def test_analyze_script_rejects_typeddict_without_definition(tmp_path, annotation):
    source = tmp_path / "sample.py"
    source.write_text(
        f"""
from typing import TypedDict


def process(value: {annotation}) -> int:
    return 1
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="must reference a defined TypedDict class"):
        analyze_script(source)


def test_analyze_script_rejects_missing_parameter_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def greet(name) -> str:
    return f"Hello {name}"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing type annotation"):
        analyze_script(source)


def test_analyze_script_rejects_unsupported_scalar_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def process_value(value: object) -> int:
    return 1
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported data type"):
        analyze_script(source)


def test_analyze_script_rejects_bytes_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def duplicate(data: bytes) -> bytes:
    return data + data
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported data type"):
        analyze_script(source)


def test_analyze_script_rejects_unsupported_container_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def process_values(values: set[int]) -> int:
    return len(values)
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported container"):
        analyze_script(source)


def test_analyze_script_rejects_unsupported_list_element_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def process_values(values: list[set[int]]) -> int:
    return len(values)
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported list element type"):
        analyze_script(source)


def test_analyze_script_rejects_bytes_list_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def duplicate(values: list[bytes]) -> list[bytes]:
    return values
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported list element type"):
        analyze_script(source)


@pytest.mark.parametrize(
    "array_annotation",
    [
        "np.ndarray",
        "np.ndarray[np.dtype[np.float64]]",
        "np.ndarray[int, np.dtype[np.float64]]",
        "np.ndarray[tuple[float], np.dtype[np.float64]]",
        "np.ndarray[tuple[int, str], np.dtype[np.float64]]",
        "np.ndarray[tuple[()], np.dtype[np.float64]]",
        "np.ndarray[tuple[int, ...], np.dtype[np.float64]]",
    ],
)
def test_analyze_script_rejects_invalid_numpy_array_shapes(tmp_path, array_annotation):
    source = tmp_path / "sample.py"
    source.write_text(
        f"def process(values: {array_annotation}) -> int:\n    return 1\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="NumPy array.*shape"):
        analyze_script(source)


def test_analyze_script_rejects_unsupported_numpy_dtypes(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
import numpy as np


def process_values(
    values: np.ndarray[tuple[int], np.dtype[np.object_]],
) -> int:
    return len(values)
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported NumPy dtype"):
        analyze_script(source)


def test_analyze_script_rejects_numpy_bytes_dtypes(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
import numpy as np


def process_values(
    values: np.ndarray[tuple[int], np.dtype[np.bytes_]],
) -> int:
    return len(values)
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported NumPy dtype"):
        analyze_script(source)


def test_analyze_script_rejects_numpy_module_array_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
import numpy


def process_values(
    values: numpy.ndarray[tuple[int], numpy.dtype[numpy.float64]],
) -> int:
    return len(values)
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported container"):
        analyze_script(source)


def test_analyze_script_rejects_unsupported_dict_output_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def return_config(value: int) -> dict:
    return {"enabled": True, "value": value}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Use a TypedDict class"):
        analyze_script(source)


def test_analyze_script_rejects_unsupported_dict_tuple_output_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def return_config(value: int) -> tuple[dict, int]:
    return {"enabled": True}, value
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Use a TypedDict class"):
        analyze_script(source)


def test_analyze_script_rejects_unsupported_dict_list_annotations(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text(
        """
def process_configs(configs: list[dict[str, int]]) -> int:
    return len(configs)
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Use a TypedDict class"):
        analyze_script(source)


def test_analyze_script_returns_empty_function_list_for_no_top_level_functions(
    tmp_path,
):
    source = tmp_path / "sample.py"
    source.write_text("VALUE = 42\n", encoding="utf-8")

    assert json.loads(analyze_script(source)) == {
        "type_definitions": [],
        "functions": [],
    }
