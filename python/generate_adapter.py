import argparse
import json
from pathlib import Path
from pprint import pformat

from analyze import analyze_script

TEMPLATE_PATH = Path(__file__).parent / "templates" / "adapter_template.py"


def generate_adapter(
    source_path: str | Path,
    output_directory: str | Path | None = None,
) -> str:
    source_path = Path(source_path).resolve()

    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    if source_path.suffix != ".py":
        raise ValueError("Source file must be a Python file.")

    if not TEMPLATE_PATH.is_file():
        raise FileNotFoundError(f"Adapter template not found: {TEMPLATE_PATH}")

    module_name = source_path.stem
    metadata = json.loads(analyze_script(source_path))
    type_definitions = {
        type_definition["name"]: type_definition["fields"]
        for type_definition in metadata["type_definitions"]
    }
    function_metadata = {
        function["name"]: {
            "input_parameters": function["input_parameters"],
            "output_parameters": function["output_parameters"],
        }
        for function in metadata["functions"]
    }

    wrappers = []

    for function in metadata["functions"]:
        function_name = function["name"]
        wrappers.append(f"""
def {function_name}(arguments):
    metadata = FUNCTION_METADATA["{function_name}"]
    parsed_arguments = _deserialize_arguments(
        arguments,
        metadata["input_parameters"],
    )
    result = {module_name}.{function_name}(*parsed_arguments)

    return _normalize_return_value(result, metadata["output_parameters"])
""".strip())

    generated_functions = "\n\n\n".join(wrappers)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    adapter_code = template.replace("{{MODULE_NAME}}", module_name)
    adapter_code = adapter_code.replace(
        "{{TYPE_DEFINITIONS}}",
        pformat(type_definitions, sort_dicts=False),
    )
    adapter_code = adapter_code.replace(
        "{{FUNCTION_METADATA}}",
        pformat(function_metadata, sort_dicts=False),
    )
    adapter_code = adapter_code.replace(
        "{{GENERATED_FUNCTIONS}}",
        generated_functions,
    )

    if output_directory is None:
        output_directory = source_path.parent
    else:
        output_directory = Path(output_directory).resolve()

    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = output_directory / "adapter.py"
    output_path.write_text(adapter_code, encoding="utf-8")

    return str(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a LabVIEW Python adapter module."
    )
    parser.add_argument("source_path")
    parser.add_argument("-o", "--output-directory")

    args = parser.parse_args()

    generated_path = generate_adapter(
        source_path=args.source_path,
        output_directory=args.output_directory,
    )

    print(f"Generated adapter: {generated_path}")
