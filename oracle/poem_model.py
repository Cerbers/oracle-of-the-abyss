from pathlib import Path
from dataclasses import dataclass
from oracle.syllable_counter import count_syllables


@dataclass
class Poem:
    text: str
    filepath: Path

    def __post_init__(self):
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")

        if not self.text.strip():
            raise ValueError("Poem text cannot be empty")

        if not isinstance(self.filepath, Path):
            raise TypeError("filepath must be a pathlib.Path object")

    @property
    def filename(self) -> str:
        return self.filepath.stem


@dataclass
class Word:
    text: str

    @property
    def syllable_variants(self) -> list[int]:
        return [count_syllables(self.text)]


@dataclass
class Line:
    text: str

    def __post_init__(self):
        if not self.text:
            raise ValueError("Line text cannot be empty")

    @property
    def break_line_string_into_words(self) -> list[Word]:
        words_in_line = self.text.split()
        return [Word(text=word) for word in words_in_line]


@dataclass
class Stanza:
    lines: list[Line]

    def __post_init__(self):
        if not self.lines:
            raise ValueError("Stanza must contain at least one Line")
