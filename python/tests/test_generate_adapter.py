import importlib.util
from pathlib import Path

import pytest

from generate_adapter import generate_adapter


def load_module_from_path(module_name, module_path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generate_adapter_writes_adapter_for_source_functions(tmp_path):
    source = tmp_path / "math_tools.py"
    source.write_text(
        """
def add(left: int, right: int) -> int:
    return left + right


def subtract(left: int, right: int) -> int:
    return left - right
""",
        encoding="utf-8",
    )

    output_path = Path(generate_adapter(source))

    assert output_path == tmp_path / "adapter.py"
    adapter_code = output_path.read_text(encoding="utf-8")
    assert "import math_tools" in adapter_code
    assert "def add(arguments):" in adapter_code
    assert "parsed_arguments = _deserialize_arguments(" in adapter_code
    assert "result = math_tools.add(*parsed_arguments)" in adapter_code
    assert "def subtract(arguments):" in adapter_code
    assert "result = math_tools.subtract(*parsed_arguments)" in adapter_code
    assert (
        'return _normalize_return_value(result, metadata["output_parameters"])'
        in adapter_code
    )


def test_generate_adapter_normalizes_scalar_and_tuple_returns(tmp_path, monkeypatch):
    source = tmp_path / "return_tools.py"
    source.write_text(
        """
def return_scalar(value: int) -> int:
    return value


def return_tuple(value: int) -> tuple[int, str]:
    return value, "ok"
""",
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    output_path = generate_adapter(source)
    adapter = load_module_from_path("generated_adapter_returns", output_path)

    assert adapter.return_scalar((3,)) == (3,)
    assert adapter.return_tuple((3,)) == (3, "ok")


def test_generate_adapter_rejects_function_without_output(tmp_path):
    source = tmp_path / "return_tools.py"
    source.write_text(
        """
def return_none(value: int) -> None:
    pass
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="at least one output parameter"):
        generate_adapter(source)


def test_generate_adapter_converts_typed_dict_clusters_in_both_directions(
    tmp_path, monkeypatch
):
    source = tmp_path / "dict_tools.py"
    source.write_text(
        """
from typing import TypedDict


class Config(TypedDict):
    message: str
    count: int


class Result(TypedDict):
    message: str
    count: int


class Measurement(TypedDict):
    value: float
    valid: bool


def echo_config(config: Config) -> Result:
    return config


def echo_measurements(measurements: list[Measurement]) -> list[Measurement]:
    return measurements


def return_tuple_with_dict(count: int) -> tuple[Result, int]:
    return {"message": "done", "count": count}, count
""",
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    output_path = generate_adapter(source)
    adapter = load_module_from_path("generated_adapter", output_path)

    dict_result = adapter.echo_config((("ready", 2),))
    list_result = adapter.echo_measurements(([(1.5, True)],))
    tuple_result = adapter.return_tuple_with_dict((7,))

    assert dict_result == (("ready", 2),)
    assert list_result == ([(1.5, True)],)
    assert tuple_result == (("done", 7), 7)


def test_generate_adapter_converts_nested_typed_dict_clusters(tmp_path, monkeypatch):
    source = tmp_path / "nested_tools.py"
    source.write_text(
        """
from typing import TypedDict


class Leaf(TypedDict):
    value: int


class Middle(TypedDict):
    leaf: Leaf
    label: str


class Root(TypedDict):
    middle: Middle
    leaf_groups: list[list[Leaf]]


def increment_nested(config: Root) -> Root:
    config["middle"]["leaf"]["value"] += 1
    config["leaf_groups"][1][0]["value"] += 10
    return config
""",
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    output_path = generate_adapter(source)
    adapter = load_module_from_path("generated_nested_adapter", output_path)

    result = adapter.increment_nested(
        (
            (
                ((5,), "sensor"),
                [[(1,), (2,)], [(3,)]],
            ),
        )
    )

    assert result == (
        (
            ((6,), "sensor"),
            [[(1,), (2,)], [(13,)]],
        ),
    )


def test_generate_adapter_rejects_unsupported_dict_annotations(tmp_path):
    source = tmp_path / "dict_tools.py"
    source.write_text(
        """
def return_dict(value: int) -> dict:
    return {"message": "ready", "value": value}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Use a TypedDict class"):
        generate_adapter(source)


def test_generate_adapter_uses_custom_output_directory(tmp_path):
    source = tmp_path / "math_tools.py"
    source.write_text(
        """
def add(left: int, right: int) -> int:
    return left + right
""",
        encoding="utf-8",
    )
    output_directory = tmp_path / "generated" / "adapters"

    output_path = Path(generate_adapter(source, output_directory))

    assert output_path == output_directory / "adapter.py"
    assert output_path.is_file()


def test_generate_adapter_raises_for_missing_source(tmp_path):
    with pytest.raises(FileNotFoundError, match="Source file not found"):
        generate_adapter(tmp_path / "missing.py")


def test_generate_adapter_raises_for_non_python_source(tmp_path):
    source = tmp_path / "notes.txt"
    source.write_text("def add(left, right): return left + right\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Source file must be a Python file"):
        generate_adapter(source)
