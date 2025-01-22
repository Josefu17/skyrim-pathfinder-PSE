"""This module contains the Prometheus converter function."""

import re


def make_prometheus_conform(string: str, max_length: int = 100) -> str:
    """
    Convert a string to a Prometheus-conform metric name.
    """
    if not string:
        raise ValueError("Input string must not be empty.")

    # mapping of special characters to their replacements
    umlaut_mapping = {"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ß": "ss"}

    # replace german umlauts and other special characters
    for char, replacement in umlaut_mapping.items():
        string = string.replace(char, replacement)

    # replace all non-alphanumeric characters with underscores
    string = re.sub(r"\W", "_", string)

    # if the string starts with a number, prepend an underscore
    if re.match(r"^\d", string):
        string = f"_{string}"

    # if the string is longer than the maximum length, truncate it
    if len(string) > max_length:
        string = string[:max_length]

    return string
