from dataclasses import dataclass
from oracle.syllable_counter import count_syllables


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
        
    def get_total_syllables(self) -> int:
        return sum(self.get_syllable_counts())

    @property
    def line_chain_of_words(self) -> list[Word]:
        words_in_line = self.text.split()
        return [Word(text=word) for word in words_in_line]

    def get_syllable_counts(self) -> list[int]:
        return [word.syllable_variants[0] for word in self.line_chain_of_words]


@dataclass
class Stanza:
    lines: list[Line]

    def __post_init__(self):
        if not self.lines:
            raise ValueError("Stanza must contain at least one Line")
    
    @property
    def stanza_text_string(self) -> str:
        return '\n'.join(line.text for line in self.lines)