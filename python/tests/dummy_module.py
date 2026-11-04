from typing import TypedDict

import numpy as np
import qrcode
from scipy import ndimage, signal


class Calibration(TypedDict):
    gain: float
    offset: float


class MeasurementConfig(TypedDict):
    calibration: Calibration
    enabled: bool
    label: str


class MeasurementResult(TypedDict):
    success: bool
    message: str
    adjusted_value: float


class ArrayConfig(TypedDict):
    values: np.ndarray[tuple[int, int], np.dtype[np.float64]]
    factor: float


class ChannelLimits(TypedDict):
    minimum: float
    maximum: float


class ChannelConfig(TypedDict):
    limits: ChannelLimits
    name: str


class DeviceConfig(TypedDict):
    channel: ChannelConfig
    enabled: bool


class SensorCalibration(TypedDict):
    gain: float
    offset: float


class SensorConfig(TypedDict):
    calibration: SensorCalibration
    serial_number: str


class AcquisitionConfig(TypedDict):
    sensor: SensorConfig
    sample_rate: float


class ExperimentConfig(TypedDict):
    acquisition: AcquisitionConfig
    operator: str


def add_integers(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a: First integer
        b: Second integer

    Returns:
        Sum of both integers
    """
    return a + b


def divide_values(a: float, b: float) -> float:
    """
    Divide two floating point numbers.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Division result
    """
    return a / b


def add_numpy_float32_values(a: np.float32, b: np.float32) -> np.float32:
    """
    Add two NumPy 32-bit floating point scalar values.

    Args:
        a: First NumPy 32-bit floating point value
        b: Second NumPy 32-bit floating point value

    Returns:
        Sum of both NumPy 32-bit floating point values
    """
    return a + b


def increment_numpy_u8_value(value: np.uint8) -> np.uint8:
    """
    Increment a NumPy unsigned 8-bit integer scalar value.

    Args:
        value: Input NumPy unsigned 8-bit integer value

    Returns:
        Incremented NumPy unsigned 8-bit integer value
    """
    return value + 1


def invert_flag(flag: bool) -> bool:
    """
    Invert a boolean value.

    Args:
        flag: Input boolean

    Returns:
        Inverted boolean
    """
    return not flag


def create_greeting(name: str) -> str:
    """
    Create a greeting string.

    Args:
        name: Person name

    Returns:
        Greeting message
    """
    return f"Hello {name}"


def increment_u8_value(value: int) -> int:
    """
    Increment an unsigned byte value.

    Args:
        value: Input unsigned byte value

    Returns:
        Incremented unsigned byte value
    """
    return value + 1


def scale_float_list(values: list[float], factor: float) -> list[float]:
    """
    Scale a list of floating point values.

    Args:
        values: Input float list
        factor: Scale factor

    Returns:
        Scaled float list
    """
    return [value * factor for value in values]


def increment_integer_list(values: list[int]) -> list[int]:
    """
    Increment every integer in a list.

    Args:
        values: Input integer list

    Returns:
        Incremented integer list
    """
    return [value + 1 for value in values]


def invert_boolean_list(values: list[bool]) -> list[bool]:
    """
    Invert every boolean in a list.

    Args:
        values: Input boolean list

    Returns:
        Inverted boolean list
    """
    return [not value for value in values]


def append_string_list(values: list[str], suffix: str) -> list[str]:
    """
    Append text to every string in a list.

    Args:
        values: Input string list
        suffix: Text to append

    Returns:
        String list with appended text
    """
    return [value + suffix for value in values]


def increment_u8_list(values: list[int]) -> list[int]:
    """
    Increment every unsigned byte value in a list.

    Args:
        values: Input unsigned byte value list

    Returns:
        Incremented unsigned byte value list
    """
    return [value + 1 for value in values]


def summarize_measurement(
    value: float,
    valid: bool,
) -> tuple[float, bool]:
    """
    Create a tuple result.

    Args:
        value: Measurement value
        valid: Measurement validity

    Returns:
        Tuple containing value and validity
    """
    return value, valid


def scale_numpy_array(
    array_in: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    factor: float,
) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
    """
    Scale a NumPy floating point array by a factor.

    Args:
        array_in: Input NumPy floating point array
        factor: Scale factor

    Returns:
        Scaled NumPy floating point array
    """
    return array_in * factor


def scale_numpy_integer_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.int64]],
    factor: int,
) -> np.ndarray[tuple[int], np.dtype[np.int64]]:
    """
    Scale a NumPy integer array by a factor.

    Args:
        array_in: Input NumPy integer array
        factor: Scale factor

    Returns:
        Scaled NumPy integer array
    """
    return array_in * factor


def scale_numpy_int8_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.int8]],
    factor: int,
) -> np.ndarray[tuple[int], np.dtype[np.int8]]:
    """
    Scale a NumPy 8-bit integer array by a factor.

    Args:
        array_in: Input NumPy 8-bit integer array
        factor: Scale factor

    Returns:
        Scaled NumPy 8-bit integer array
    """
    return array_in * factor


def scale_numpy_int16_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.int16]],
    factor: int,
) -> np.ndarray[tuple[int], np.dtype[np.int16]]:
    """
    Scale a NumPy 16-bit integer array by a factor.

    Args:
        array_in: Input NumPy 16-bit integer array
        factor: Scale factor

    Returns:
        Scaled NumPy 16-bit integer array
    """
    return array_in * factor


def scale_numpy_int32_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.int32]],
    factor: int,
) -> np.ndarray[tuple[int], np.dtype[np.int32]]:
    """
    Scale a NumPy 32-bit integer array by a factor.

    Args:
        array_in: Input NumPy 32-bit integer array
        factor: Scale factor

    Returns:
        Scaled NumPy 32-bit integer array
    """
    return array_in * factor


def scale_numpy_uint8_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.uint8]],
    factor: int,
) -> np.ndarray[tuple[int], np.dtype[np.uint8]]:
    """
    Scale a NumPy unsigned 8-bit integer array by a factor.

    Args:
        array_in: Input NumPy unsigned 8-bit integer array
        factor: Scale factor

    Returns:
        Scaled NumPy unsigned 8-bit integer array
    """
    return array_in * factor


def scale_numpy_uint16_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.uint16]],
    factor: int,
) -> np.ndarray[tuple[int], np.dtype[np.uint16]]:
    """
    Scale a NumPy unsigned 16-bit integer array by a factor.

    Args:
        array_in: Input NumPy unsigned 16-bit integer array
        factor: Scale factor

    Returns:
        Scaled NumPy unsigned 16-bit integer array
    """
    return array_in * factor


def scale_numpy_uint32_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.uint32]],
    factor: int,
) -> np.ndarray[tuple[int], np.dtype[np.uint32]]:
    """
    Scale a NumPy unsigned 32-bit integer array by a factor.

    Args:
        array_in: Input NumPy unsigned 32-bit integer array
        factor: Scale factor

    Returns:
        Scaled NumPy unsigned 32-bit integer array
    """
    return array_in * factor


def scale_numpy_uint64_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.uint64]],
    factor: int,
) -> np.ndarray[tuple[int], np.dtype[np.uint64]]:
    """
    Scale a NumPy unsigned 64-bit integer array by a factor.

    Args:
        array_in: Input NumPy unsigned 64-bit integer array
        factor: Scale factor

    Returns:
        Scaled NumPy unsigned 64-bit integer array
    """
    return array_in * factor


def scale_numpy_float32_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.float32]],
    factor: float,
) -> np.ndarray[tuple[int], np.dtype[np.float32]]:
    """
    Scale a NumPy 32-bit floating point array by a factor.

    Args:
        array_in: Input NumPy 32-bit floating point array
        factor: Scale factor

    Returns:
        Scaled NumPy 32-bit floating point array
    """
    return array_in * factor


def invert_numpy_boolean_array(
    array_in: np.ndarray[tuple[int, int, int], np.dtype[np.bool_]],
) -> np.ndarray[tuple[int, int, int], np.dtype[np.bool_]]:
    """
    Invert a NumPy boolean array.

    Args:
        array_in: Input NumPy boolean array

    Returns:
        Inverted NumPy boolean array
    """
    return np.logical_not(array_in)


def append_numpy_string_array(
    array_in: np.ndarray[tuple[int], np.dtype[np.str_]],
    suffix: str,
) -> np.ndarray[tuple[int], np.dtype[np.str_]]:
    """
    Append text to each element in a NumPy string array.

    Args:
        array_in: Input NumPy string array
        suffix: Text to append

    Returns:
        NumPy string array with appended text
    """
    return np.char.add(array_in, suffix)


def increment_numpy_u8_array(
    array_in: np.ndarray[tuple[int, int, int], np.dtype[np.uint8]],
) -> np.ndarray[tuple[int, int, int], np.dtype[np.uint8]]:
    """
    Increment each element in a NumPy unsigned 8-bit integer array.

    Args:
        array_in: Input NumPy unsigned 8-bit integer array

    Returns:
        Incremented NumPy unsigned 8-bit integer array
    """
    return array_in + 1


def process_measurement_config(config: MeasurementConfig) -> MeasurementResult:
    """
    Process a nested measurement configuration dictionary.

    Args:
        config: Measurement configuration

    Returns:
        Measurement result dictionary
    """
    calibration = config["calibration"]
    adjusted_value = calibration["gain"] + calibration["offset"]
    success = config["enabled"] and adjusted_value > 0

    return {
        "success": success,
        "message": config["label"],
        "adjusted_value": adjusted_value,
    }


def process_measurement_configs(
    configs: list[MeasurementConfig],
) -> list[MeasurementResult]:
    """
    Process a list of nested measurement configuration dictionaries.

    Args:
        configs: Measurement configuration dictionaries

    Returns:
        Measurement result dictionaries
    """
    return [process_measurement_config(config) for config in configs]


def scale_array_from_config(config: ArrayConfig) -> ArrayConfig:
    """
    Scale an array stored in a dictionary.

    Args:
        config: Array configuration dictionary

    Returns:
        Array configuration dictionary with scaled values
    """
    return {
        "values": config["values"] * config["factor"],
        "factor": config["factor"],
    }


def process_device_config(config: DeviceConfig) -> MeasurementResult:
    """
    Process a device configuration with two nested dictionary levels.

    Args:
        config: Device configuration

    Returns:
        Measurement result dictionary
    """
    limits = config["channel"]["limits"]
    valid_limits = limits["minimum"] < limits["maximum"]

    return {
        "success": config["enabled"] and valid_limits,
        "message": config["channel"]["name"],
        "adjusted_value": limits["maximum"] - limits["minimum"],
    }


def process_experiment_config(config: ExperimentConfig) -> MeasurementResult:
    """
    Process an experiment configuration with three nested dictionary levels.

    Args:
        config: Experiment configuration

    Returns:
        Measurement result dictionary
    """
    calibration = config["acquisition"]["sensor"]["calibration"]
    adjusted_value = calibration["gain"] + calibration["offset"]

    return {
        "success": config["acquisition"]["sample_rate"] > 0,
        "message": config["operator"],
        "adjusted_value": adjusted_value,
    }


def mixed_example(
    count: int,
    threshold: float,
    enabled: bool,
    label: str,
    values: list[float],
) -> tuple[bool, str]:
    """
    Complex example function using multiple supported types.

    Args:
        count: Number of iterations
        threshold: Threshold value
        enabled: Enable flag
        label: Text label
        values: Numeric values

    Returns:
        Tuple containing status and message
    """
    total = sum(values)
    success = enabled and total > threshold and count > 0
    message = f"Label={label}, Total={total}"

    return success, message


def smooth_detrended_signal(
    values: np.ndarray[tuple[int], np.dtype[np.float64]],
    window_length: int,
    polynomial_order: int,
) -> np.ndarray[tuple[int], np.dtype[np.float64]]:
    """Remove a linear trend, then smooth a one-dimensional float signal."""
    detrended = signal.detrend(values)
    return signal.savgol_filter(detrended, window_length, polynomial_order)


def replace_integer_spikes(
    values: np.ndarray[tuple[int], np.dtype[np.int64]],
    window_size: int,
    threshold: int,
) -> np.ndarray[tuple[int], np.dtype[np.int64]]:
    """Replace one-dimensional integer outliers with their local median."""
    baseline = ndimage.median_filter(values, size=window_size)
    return np.where(np.abs(values - baseline) > threshold, baseline, values)


def sharpen_float_grid(
    values: np.ndarray[tuple[int, int], np.dtype[np.float64]],
    sigma: float,
    strength: float,
) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
    """Smooth a two-dimensional float grid, then enhance its edges."""
    smoothed = ndimage.gaussian_filter(values, sigma=sigma)
    edges = ndimage.laplace(smoothed)
    return smoothed - strength * edges


def close_integer_grid(
    values: np.ndarray[tuple[int, int], np.dtype[np.int64]],
    window_size: int,
) -> np.ndarray[tuple[int, int], np.dtype[np.int64]]:
    """Fill small low-valued gaps in a two-dimensional integer grid."""
    expanded = ndimage.maximum_filter(values, size=window_size)
    return ndimage.minimum_filter(expanded, size=window_size)


def create_url_qr_code(
    url: str,
) -> np.ndarray[tuple[int, int], np.dtype[np.uint8]]:
    """Encode a URL as a 2D array of QR modules (1 for dark, 0 for light)."""
    qr = qrcode.QRCode(border=4)
    qr.add_data(url)
    qr.make(fit=True)
    return np.array(qr.get_matrix(), dtype=np.uint8)


# Scalar coverage for every supported NumPy data type.
def invert_numpy_boolean_value(value: np.bool_) -> np.bool_:
    """Invert a NumPy boolean scalar."""
    return np.bool_(not value)


def increment_numpy_int8_value(value: np.int8) -> np.int8:
    """Increment a NumPy signed 8-bit integer scalar."""
    return np.int8(value + 1)


def increment_numpy_int16_value(value: np.int16) -> np.int16:
    """Increment a NumPy signed 16-bit integer scalar."""
    return np.int16(value + 1)


def increment_numpy_int32_value(value: np.int32) -> np.int32:
    """Increment a NumPy signed 32-bit integer scalar."""
    return np.int32(value + 1)


def increment_numpy_int64_value(value: np.int64) -> np.int64:
    """Increment a NumPy signed 64-bit integer scalar."""
    return np.int64(value + 1)


def increment_numpy_uint16_value(value: np.uint16) -> np.uint16:
    """Increment a NumPy unsigned 16-bit integer scalar."""
    return np.uint16(value + 1)


def increment_numpy_uint32_value(value: np.uint32) -> np.uint32:
    """Increment a NumPy unsigned 32-bit integer scalar."""
    return np.uint32(value + 1)


def increment_numpy_uint64_value(value: np.uint64) -> np.uint64:
    """Increment a NumPy unsigned 64-bit integer scalar."""
    return np.uint64(value + 1)


def increment_numpy_float64_value(value: np.float64) -> np.float64:
    """Increment a NumPy 64-bit floating-point scalar."""
    return np.float64(value + 1)


def append_numpy_string_value(value: np.str_) -> np.str_:
    """Append text to a NumPy string scalar."""
    return np.str_(value + "_processed")
