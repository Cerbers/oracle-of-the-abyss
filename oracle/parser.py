"""Parser module for converting poem text into structured stanzas.

This module provides functionality to parse raw poem text into
a structured format of stanzas and lines, handling title detection
and blank line separation.
"""

from oracle.utils import check_for_title_line

# TODO improve parse_into_stanzas to handle title cases when first line of other stanzas matches filename


def parse_into_stanzas(poem_text: str, poem_name: str) -> list[list[str]]:
    """Parse poem text into a list of stanzas, each containing a list of lines.

    Splits poem text by blank lines to identify stanza boundaries. Handles
    multiple consecutive blank lines as a single separator. If the first line
    appears to be a title (based on formatting or filename match), it is
    automatically removed.

    Args:
        poem_text: The raw text content of the poem.
        poem_name: The filename (without extension) to use for title detection.

    Returns:
        A list of stanzas, where each stanza is a list of non-empty line strings.
        Leading and trailing whitespace is stripped from each line.

    Example:
        >>> text = '"Voidborn"\\nFirst line\\n\\nSecond stanza'
        >>> parse_into_stanzas(text, "Voidborn")
        [['First line'], ['Second stanza']]
    """
    cleaned_text = '\n'.join(line.strip() for line in poem_text.splitlines())

    stanzas = cleaned_text.split('\n\n')

    result = []
    for stanza in stanzas:
        lines = [line.strip() for line in stanza.split('\n') if line.strip()]
        if check_for_title_line(lines[0], poem_name):
            lines.pop(0)
        if lines:
            result.append(lines)
    return result