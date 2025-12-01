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