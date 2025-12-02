"""Poem analysis module for extracting structural information from poems.

This module provides functionality to analyze poems and extract
structural information such as stanza text, line counts, and syllable patterns.
"""

from oracle.poem_model import Poem, Line, Stanza


def analyze_poem(poem: Poem) -> dict[str, list]:
    """Analyze a poem and extract its structural information.

    Takes a Poem object and processes each stanza to extract text content,
    line counts, and syllable counts per line. The function converts raw
    string stanzas into domain objects (Stanza, Line) for processing.

    Args:
        poem: A Poem object containing the poem text and metadata.

    Returns:
        A dictionary containing:
            - 'stanza_texts': List of strings, each being the full text of a stanza
              with lines separated by newlines.
            - 'line_counts': List of integers representing the number of lines
              in each stanza.
            - 'syllables_per_line': List of lists of integers, where each inner
              list contains the syllable count for each line in a stanza.

    Example:
        >>> poem = Poem(text="Hello world\\n\\nGoodbye moon", filepath=Path("test.txt"))
        >>> result = analyze_poem(poem)
        >>> result['line_counts']
        [1, 1]
    """
    stanza_texts = []
    line_counts = []
    syllables_per_line = []

    # Convert raw string stanzas into Stanza objects
    for stanza_lines in poem.stanzas:  # list[list[str]]
        # Create Line objects from strings
        line_objects = [Line(text=line) for line in stanza_lines]

        # Create Stanza object
        stanza_obj = Stanza(lines=line_objects)

        # Now work with the object model
        stanza_texts.append(stanza_obj.stanza_text_string)
        line_counts.append(len(stanza_obj.lines))

        # Get syllable counts from Line objects
        stanza_syllables = [line.get_total_syllables() for line in stanza_obj.lines]
        syllables_per_line.append(stanza_syllables)

    return {
        'stanza_texts': stanza_texts,
        'line_counts': line_counts,
        'syllables_per_line': syllables_per_line
    }