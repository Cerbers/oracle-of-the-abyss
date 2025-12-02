"""Utility functions for poem processing.

This module provides helper functions used across the poem analyzer,
including title line detection and other text processing utilities.
"""


def check_for_title_line(line: str, filename: str) -> bool:
    """Determine if a line is likely a poem title.

    Checks various formatting conventions commonly used to denote
    poem titles, including quoted text, all-caps text, and lines
    that match the filename.

    Args:
        line: The text line to check for title characteristics.
        filename: The poem filename (without extension) to compare against.

    Returns:
        True if the line appears to be a title, False otherwise.

    Title detection rules:
        - Line enclosed in double quotes ("Title")
        - Line enclosed in single quotes ('Title')
        - Line is entirely uppercase (TITLE)
        - Line matches the filename exactly

    Example:
        >>> check_for_title_line('"The Raven"', "The Raven")
        True
        >>> check_for_title_line("Once upon a midnight dreary", "The Raven")
        False
    """
    stripped = line.strip()

    if stripped.startswith('"') and stripped.endswith('"'):
        return True

    if stripped.startswith("'") and stripped.endswith("'"):
        return True

    if stripped.isupper():
        return True

    if stripped == filename:
        return True

    return False
