from typing import TypedDict

import numpy as np


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
