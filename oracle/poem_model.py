"""
Poem model module for poem analysis.
"""


from pathlib import Path
from dataclasses import dataclass
from functools import cached_property

from oracle.parser import parse_into_stanzas
from oracle.domain_objects import Stanza



@dataclass
class Poem:
    """
    Represents a poem with its text and filepath.
    
    Attributes:
        text (str): The text of the poem.
        filepath (Path): The filepath of the poem.
    
    Methods:
        filename: Returns the filename of the poem.
        stanzas: Returns the list of stanzas in the poem.
    """
    text: str
    filepath: Path

    def __post_init__(self) -> None:
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")

        if not self.text.strip():
            raise ValueError("Poem text cannot be empty")

        if not isinstance(self.filepath, Path):
            raise TypeError("filepath must be a pathlib.Path object")

    @property
    def filename(self) -> str:
        """Return the filename of the poem."""
        return self.filepath.stem
    
    @cached_property
    def stanzas(self) -> list[Stanza]:
        """Return the list of stanzas in the poem."""
        return parse_into_stanzas(self.text, self.filename)