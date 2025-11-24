from pathlib import Path
from dataclasses import dataclass



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