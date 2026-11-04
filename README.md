# py2vi

**Turn Python code into ready-to-use LabVIEW libraries.**

py2vi is an open-source command-line tool that automatically generates LabVIEW wrapper VIs from Python code.

Provide a Python module with supported type annotations, and py2vi generates a LabVIEW project containing wrapper VIs, type definitions, and the components needed for Python integration. Build the project into a Packed Project Library (PPL) for use in LabVIEW—without manually configuring Python Nodes or wrapper VIs.

## 🎬 Demo

https://github.com/user-attachments/assets/bd6e0862-c597-4e75-a998-ad1d3115a074


## 🚀 Quick Start

1. Install py2vi using [VI Package Manager (VIPM)](https://www.vipm.io/).

2. Prepare a Python module with [supported type annotations](#supported-python-code).

3. Create a compatible Python virtual environment and configure `py2vi_global_venv`.

4. Generate your LabVIEW project:

   ```powershell
   g-cli <g-cli-options> py2vi -- -module <path-to-python-file> -output <path-to-output-folder> -clear-cache
   ```

5. Build the generated Packed Project Library (PPL) and use it in LabVIEW.

For detailed instructions, see [Usage](#usage).


## ⚙️ How Does It Work?

py2vi combines Python's Abstract Syntax Tree (AST) analysis with LabVIEW VI Scripting to automatically generate LabVIEW wrappers for Python functions.

The generation process consists of the following steps:

### 1. Python Code Analysis

The Python source code is analyzed using Python's built-in `ast` module. The analyzer extracts metadata about:

* **Functions:** Names, docstrings, input parameters, and return values.
* **Parameters:** Names, data types, container types, and array dimensions.
* **Type definitions:** `TypedDict` structures, including nested dependencies.

The extracted information is serialized into a JSON string containing two main lists: `type_definitions` and `functions`.

In addition to user-defined `TypedDict` structures, py2vi automatically creates type definition metadata for each function's input and output parameters. These will later become LabVIEW clusters.

Since LabVIEW type definitions may reference other type definitions, their creation order matters. py2vi resolves these dependencies using a topological sort, ensuring that referenced types are created before the types that depend on them.

Circular dependencies are detected and rejected with an error message.

### 2. Python Adapter Generation

A Python adapter module is automatically generated to handle communication between LabVIEW and the original Python functions.

The adapter provides wrapper functions that deserialize incoming arguments, invoke the corresponding Python functions, and normalize their return values into a format compatible with LabVIEW's Python Node.

This allows the generated LabVIEW VIs to use a consistent interface regardless of the original Python function signatures.

### 3. LabVIEW Code Generation

LabVIEW reads the generated JSON metadata and uses VI Scripting to create the required components.

First, all LabVIEW type definitions are generated in dependency order.

Next, individual wrapper VIs are created from a predefined VI template. The template's input and output controls are replaced with the corresponding generated type definitions.

Each generated VI provides a LabVIEW interface to its associated Python function.

During generation, py2vi calculates the SHA-512 hashes of the Python adapter and the original Python module and embeds them into the LabVIEW code for runtime integrity verification.

### 4. Project Integration

Finally, all generated VIs and type definitions are added to the LabVIEW project and included in its Packed Project Library (PPL) build specification.

The resulting project is ready to be built into a PPL, which can then be used in other LabVIEW applications.

## 🔒 Python Code Integrity Verification

py2vi includes an integrity verification mechanism to detect changes to the generated Python adapter and the original Python module.

During library generation, py2vi calculates the SHA-512 hashes of both Python files and embeds them as constants directly into a LabVIEW VI.

When the project is built into a Packed Project Library (PPL), these reference hashes become part of the compiled library.

Before executing Python code, the generated LabVIEW wrapper verifies the integrity of both files by comparing their current SHA-512 hashes against the embedded reference hashes.

If either hash does not match, execution is aborted and an error is returned.

**Note:** This mechanism protects the integrity of the adapter and the original Python module, but does not verify imported dependencies or protect against replacement of the PPL itself.

## 🐍 Supported Python Code

py2vi uses Python [type annotations](https://typing.python.org/en/latest/spec/annotations.html) to automatically generate LabVIEW VIs and type definitions. To ensure compatibility, the Python source code must follow a few conventions.

You can, of course, use your favorite LLM to generate Python code compatible with py2vi. The following prompt can help:

> Generate a Python module compatible with py2vi. Follow these requirements:
>
> * Define functions at the module level.
> * Give every function at least one input parameter. Use only ordinary parameters (no positional-only or keyword-only parameters, `*args`, or `**kwargs`).
> * Use explicit type annotations for all input parameters. Give every function at least one output value and an explicit return type annotation. Do not use `-> None`.
> * Supported scalar types: `int`, `float`, `bool`, `str`, `np.bool_`, `np.int8`, `np.int16`, `np.int32`, `np.int64`, `np.uint8`, `np.uint16`, `np.uint32`, `np.uint64`, `np.float32`, `np.float64`, and `np.str_`.
> * Supported containers: `list[T]`, nested lists, and `np.ndarray` with explicitly annotated dimensions and dtype.
> * Use `TypedDict` for structured data. Nested `TypedDict` definitions are supported, but circular dependencies are not.
> * Use `tuple[T1, T2, ...]` for multiple return values.
> * Do not use `Any`, `Optional`, `Union`, `dict`, `set`, `bytes`, complex numbers, custom classes, or tuples as input parameters.
> * Do not use class methods or asynchronous functions.
> * Return only the Python code.
>
> **Task:** [Describe what the Python module should do.]

The following sections describe these requirements in more detail.

### General Requirements

* The source code must be provided as a `.py` file.
* Functions must be defined at the module level.
* Every function must have at least one input parameter.
* Functions must use only ordinary parameters. Positional-only (`/`), keyword-only (`*`), `*args`, and `**kwargs` parameters are not supported.
* All function input parameters must have explicit type annotations.
* Every function must return at least one value and have an explicit return type annotation. Functions annotated `-> None` are not supported.
* Only supported data types and containers can be used in function signatures and `TypedDict` definitions.
* Class methods and asynchronous functions are not supported.

For a complete example, see [dummy_module.py](./python/tests/dummy_module.py), which is also used in the project's CI pipeline for automated testing.

### Supported Data Types

The following Python data types are supported:

| Category                | Python Type Annotations                           |
| ----------------------- | ------------------------------------------------- |
| Integer                 | `int`                                             |
| Floating-point          | `float`                                           |
| Boolean                 | `bool`                                            |
| String                  | `str`                                             |
| NumPy Boolean           | `np.bool_`                                        |
| NumPy signed integers   | `np.int8`, `np.int16`, `np.int32`, `np.int64`     |
| NumPy unsigned integers | `np.uint8`, `np.uint16`, `np.uint32`, `np.uint64` |
| NumPy floating-point    | `np.float32`, `np.float64`                        |
| NumPy string            | `np.str_`                                         |
| Structured data         | `TypedDict`                                       |

### Lists and Arrays

py2vi supports Python lists and NumPy arrays, including multidimensional arrays. For example, 8-bit grayscale images can be passed as 2D `np.uint8` arrays.

**Python lists:**

```python
def process_values(values: list[float]) -> list[float]:
    return [value * 2 for value in values]
```

Nested lists are also supported:

```python
def process_matrix(matrix: list[list[float]]) -> list[list[float]]:
    return matrix
```

**NumPy arrays:**

NumPy arrays must specify their dimensions and element type using type annotations.

```python
import numpy as np

def process_array(
    values: np.ndarray[tuple[int, int], np.dtype[np.float64]]
) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
    return values * 2
```

In this example, the annotation describes a two-dimensional array of 64-bit floating-point values.

### Structured Data (TypedDict)

Python dictionaries can be represented as LabVIEW clusters using `TypedDict`.

```python
from typing import TypedDict

class Measurement(TypedDict):
    value: float
    valid: bool

def evaluate(measurement: Measurement) -> Measurement:
    return measurement
```

py2vi automatically generates the corresponding LabVIEW type definitions.

Nested `TypedDict` definitions and lists of `TypedDict` objects are also supported. Circular dependencies between `TypedDict` definitions are not allowed.

Regular Python dictionaries (`dict`, `dict[str, int]`, etc.) are not supported because their structure cannot be reliably mapped to a fixed LabVIEW cluster.

### Function Return Values

Every function must return at least one value. A function may return a single value or multiple values.

**Single return value:**

```python
def add(a: int, b: int) -> int:
    return a + b
```

**Multiple return values:**

Use a tuple annotation to define multiple outputs.

```python
def calculate(a: float, b: float) -> tuple[float, float]:
    return a + b, a - b
```

### Limitations

The following are currently not supported:

* Regular dictionaries (`dict`)
* Optional and union types (`Optional`, `Union`, `int | None`)
* `Any`
* Sets (`set`)
* Byte sequences (`bytes`)
* Complex numbers (`complex`, `np.complex64`, `np.complex128`)
* Custom classes other than `TypedDict`
* Tuples as input parameters
* Functions without a return value (`-> None`)
* Class methods and asynchronous functions

Byte sequences can instead be represented using arrays of unsigned 8-bit integers (`np.uint8`), provided the Python function accepts that representation.

## 🧪 Python Virtual Environments

py2vi is designed to work with Python virtual environments. Both the generation tool and the generated LabVIEW libraries use virtual environments to manage their Python dependencies.

### Requirements

A Python virtual environment must be created before running py2vi.

The Python version must be compatible with the LabVIEW Python Node. Refer to the [LabVIEW Python Node documentation](https://www.ni.com/docs/de-DE/bundle/labview-api-ref/page/functions/python-node.html).

Additional Python packages, such as NumPy, are only required when executing generated libraries whose Python modules depend on them. They are not required for code generation.

### Global Virtual Environment

py2vi uses the environment variable `py2vi_global_venv` to locate its global Python virtual environment.

The variable must contain the absolute path to the virtual environment directory (typically `.venv`).

**Windows (PowerShell)**

Set the environment variable persistently for the current user:

```powershell
[Environment]::SetEnvironmentVariable(
    "py2vi_global_venv",
    (Resolve-Path "C:\path\to\.venv").Path,
    "User"
)
```

The global virtual environment is used during py2vi execution and can also be used by the generated LabVIEW libraries.

### Library-Specific Virtual Environments

Generated Packed Project Libraries can use either the global environment or a dedicated environment.

For a library named `MyLibrary`, py2vi supports the following environment variables:

| Environment variable          | Purpose                                                    |
| ----------------------------- | ---------------------------------------------------------- |
| `py2vi_global_venv`           | Global environment shared by py2vi and generated libraries |
| `py2vi_MyLibrary_lvlibp_venv` | Dedicated environment for `MyLibrary`                      |

A library-specific environment allows each generated PPL to use its own Python dependencies independently of other libraries. If a library-specific environment variable is defined, it takes precedence over `py2vi_global_venv`. Otherwise, the library falls back to the global virtual environment.

The specified directory must contain an existing virtual environment with the dependencies required by the corresponding Python module.

**Note:** On Windows, persistent user environment variables become available to newly started processes.

## 🛠️ Usage

py2vi is executed using the [G-CLI](https://github.com/ni/g-cli) command-line interface.

### 1. Installation

Install py2vi using [VI Package Manager (VIPM)](https://www.vipm.io/package/hasbun_wood_engineering_lib_py2vi/).

After installation, configure a Python virtual environment as described below.

### 2. Prepare the Python Module

Create a Python module containing the functions you want to use in LabVIEW.

Make sure the module follows the conventions described in [Supported Python Code](#supported-python-code).

### 3. Set Up the Python Virtual Environment

Create a Python virtual environment using [uv](https://docs.astral.sh/uv/):

```powershell
uv venv --python 3.12.7
```

If required, install the dependencies of your Python module (e.g., NumPy):

```powershell
uv pip install numpy
```

Configure the `py2vi_global_venv` environment variable as described in [Python Virtual Environments](#python-virtual-environments).

### 4. Run py2vi

Execute py2vi using G-CLI:

```powershell
g-cli <g-cli-options> py2vi -- -module <path-to-python-file> -output <path-to-output-folder>
```

Replace the placeholders with the corresponding paths.

The `-module` and `-output` parameters are required. All other parameters are optional.

> **Help**: To display the available command-line parameters and usage information, run:
> ```powershell 
> g-cli <g-cli-options> py2vi -- -help
> ```

**Command-Line Parameters**

| Parameter      | Required | Default   | Description                                                                               |
| -------------- | -------- | --------- | ------------------------------------------------------------------------------------------|
| `-module`      | Yes      | —         | Path to the source Python module.                                                         |
| `-output`      | Yes      | —         | Output directory for the generated LabVIEW project.                                       |
| `-timeout`     | No       | `600`     | Maximum execution time in seconds.                                                        |
| `-version`     | No       | `0.0.0.0` | Version assigned to the PPL build specification.                                          |
| `-clear-cache` | No       | `False`   | Clears the compiled object cache. Required when building the generated PPL.               |
| `-log-file`    | No       | —         | Path to the log file.                                                                     |
| `-help`        | No       | —         | Display usage information and parameters.                                                 |

For example:

```powershell
g-cli <g-cli-options> py2vi -- -module "C:\Projects\MyLibrary\module.py" -output "C:\Projects\MyLibrary\generated" -clear-cache
```

**Important:** If you intend to build the generated PPL, run py2vi with the `-clear-cache` option. This clears LabVIEW's compiled object cache and prevents build failures caused by cached compiled code.


### 5. Build the Packed Project Library

After successful execution, py2vi generates a LabVIEW project containing the wrapper VIs, type definitions, and the necessary Python integration components.

The project includes a Packed Project Library (PPL) build specification named `Python Module PPL`.

You can build the PPL from the command line using either [LVBuildSpec for G CLI](https://www.vipm.io/package/sas_workshops_lib_lvbuildspec_for_g_cli/) or [LabVIEWCLI](https://www.ni.com/docs/de-DE/bundle/labview/page/predefined-command-line-operations.html#d102709e315).

#### LVBuildSpec for G CLI

Install [LVBuildSpec for G CLI](https://www.vipm.io/package/sas_workshops_lib_lvbuildspec_for_g_cli/) from VIPM.io.

This tool allows you to specify the PPL version directly during the build process:

```powershell
g-cli <g-cli-options> lvbuildspec -- --project <path-to-generated-project> --buildspec "Python Module PPL" --version <your-version>
```

#### LabVIEWCLI

When using LabVIEWCLI, specify the desired PPL version using the `-version` parameter when running py2vi, since `ExecuteBuildSpec` does not support setting the version during the build process.

```powershell
LabVIEWCLI -OperationName ExecuteBuildSpec -ProjectPath <path-to-generated-project>
```

> Replace `<path-to-generated-project>` with the full path to the generated `.lvproj` file.

The resulting PPL can then be integrated into other LabVIEW applications.

## 📦 Dependencies

py2vi uses several third-party libraries for code generation and development. A complete list of these dependencies and their licenses is available in [THIRD_PARTY_LICENSES](./THIRD_PARTY_LICENSES).

Developers who want to modify or contribute to py2vi should install the required development dependencies using the [py2vi.dragon](./labview/py2vi.dragon) file included in the repository.

NumPy is not bundled with py2vi and is not required for code generation, even when NumPy data types are used. However, NumPy must be installed in the Python virtual environment when executing Python modules that depend on it.

The dependencies listed in `THIRD_PARTY_LICENSES` apply to py2vi itself. The generated LabVIEW code has no additional LabVIEW package dependencies, but requires a compatible Python environment containing the dependencies of the original Python module.

**Note:** GitHub Actions builds the LabVIEW Docker image locally for each CI job instead of pulling it from a container registry to avoid redistributing NI LabVIEW software.

## ⚠️ Custom Error Codes

| Error Code | Error Message | Description |
|---|---|---|
| -8059 | File Execution not authorized | SHA-512 hash verification failed for `module.py` or `adapter.py`. |
| -8058 | The provided new root folder does not lie inside the current root. | |
| -8057 | LabVIEWCLI Argument missing | |
| -8056 | Specified target must be a directory. | |
| -8055 | Invalid project element extension | |
| -8054 | Project item not found. | |
| -8053 | Python Executable does not exist. | |
| -8052 | Invalid venv path | Virtual environment path validation failed. |
| -8051 | Invalid environment variable name | Environment variable name validation failed. |
| -8050 | Invalid data type | |
