"""Poem domain model module containing dataclasses for poem structure.

This module defines the core domain objects for representing poems:
Poem, Stanza, Line, and Word. These classes provide structured access
to poem content and automatic syllable counting functionality.
"""

from pathlib import Path
from dataclasses import dataclass
from oracle.parser import parse_into_stanzas
from oracle.syllable_counter import count_syllables
from functools import cached_property


@dataclass
class Poem:
    """Represents a complete poem with its text and file metadata.

    A Poem is the top-level container for poem content. It validates
    that the text is non-empty and provides access to parsed stanzas.

    Attributes:
        text: The full raw text content of the poem.
        filepath: The Path object pointing to the poem's source file.
    """

    text: str
    filepath: Path

    def __post_init__(self):
        """Validate poem initialization parameters.

        Raises:
            TypeError: If text is not a string or filepath is not a Path object.
            ValueError: If the poem text is empty or contains only whitespace.
        """
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")

        if not self.text.strip():
            raise ValueError("Poem text cannot be empty")

        if not isinstance(self.filepath, Path):
            raise TypeError("filepath must be a pathlib.Path object")

    @property
    def filename(self) -> str:
        """Return the filename without extension.

        Returns:
            The stem (filename without extension) of the filepath.
        """
        return self.filepath.stem

    @cached_property
    def stanzas(self) -> list[list[str]]:
        """Parse and return the poem as a list of stanzas.

        Uses the parser module to split the poem text into stanzas,
        with each stanza being a list of line strings. The result
        is cached after the first access.

        Returns:
            A list of stanzas, where each stanza is a list of line strings.
        """
        return parse_into_stanzas(self.text, self.filename)


@dataclass
class Word:
    """Represents a single word with syllable counting capability.

    A Word wraps a text string and provides access to syllable count
    variants for that word.

    Attributes:
        text: The word text (may include punctuation).
    """

    text: str

    @property
    def syllable_variants(self) -> list[int]:
        """Return possible syllable counts for this word.

        Currently returns a single-element list with the syllable count
        from the syllable counter. May be extended in the future to
        support multiple pronunciation variants.

        Returns:
            A list containing the syllable count(s) for this word.
        """
        return [count_syllables(self.text)]


@dataclass
class Line:
    """Represents a single line of poetry.

    A Line wraps a text string and provides functionality to break
    the line into words and calculate syllable counts.

    Attributes:
        text: The text content of the line.
    """

    text: str

    def __post_init__(self):
        """Validate that the line is not empty.

        Raises:
            ValueError: If the line text is empty.
        """
        if not self.text:
            raise ValueError("Line text cannot be empty")

    def get_total_syllables(self) -> int:
        """Calculate the total number of syllables in the line.

        Returns:
            The sum of syllable counts for all words in the line.
        """
        return sum(self.get_syllable_counts())

    @property
    def line_chain_of_words(self) -> list[Word]:
        """Break the line into a list of Word objects.

        Splits the line text on whitespace and creates a Word object
        for each token.

        Returns:
            A list of Word objects representing each word in the line.
        """
        words_in_line = self.text.split()
        return [Word(text=word) for word in words_in_line]

    def get_syllable_counts(self) -> list[int]:
        """Get the syllable count for each word in the line.

        Returns:
            A list of integers representing the syllable count
            for each word in order.
        """
        return [word.syllable_variants[0] for word in self.line_chain_of_words]


@dataclass
class Stanza:
    """Represents a stanza containing multiple lines.

    A Stanza is a collection of Line objects that form a unit
    within a poem. It provides access to the combined text
    representation of all lines.

    Attributes:
        lines: A list of Line objects making up the stanza.
    """

    lines: list[Line]

    def __post_init__(self):
        """Validate that the stanza has at least one line.

        Raises:
            ValueError: If the stanza has no lines.
        """
        if not self.lines:
            raise ValueError("Stanza must contain at least one Line")

    @property
    def stanza_text_string(self) -> str:
        """Get the complete text of the stanza.

        Joins all line texts with newline characters to produce
        a single string representation of the stanza.

        Returns:
            The full stanza text with lines separated by newlines.
        """
        return '\n'.join(line.text for line in self.lines)