from dataclasses import dataclass
from functools import cached_property
from oracle.syllable_counter import count_syllables
from typing import cast
from oracle.syllable_counter import LETTERS

@dataclass
class Word:
    text: str

    @property
    def syllable_variants(self) -> list[int]:
        return count_syllables(self.text)


@dataclass
class Line:
    text: str

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("Line text cannot be empty")
        
        # Used by default in analyzer
    def get_total_syllables(self) -> int:
        """Calculate total syllables for the line (sum of first variants)."""
        counts = self.get_syllable_counts(use_all_variants=False)
        return sum(cast(list[int], counts))
    
        # To be used by syllable matching pattern
    def get_all_syllable_variants(self) -> list[list[int]]:
        """Get all unique syllable variants per word for pattern analysis."""
        return cast(list[list[int]], self.get_syllable_counts(use_all_variants=True))

    def get_syllable_counts(self, use_all_variants: bool = False) -> list[int] | list[list[int]]:
        """
        Get syllable counts for words in the line.

        Args:
            use_all_variants: If False (default), returns first variant only.
                             If True, returns all unique variants per word.

        Returns:
            When False: [1, 2, 1] (first variant per word)
            When True: [[1], [2,1], [1]] (unique variants per word)
        """
        if use_all_variants:
            return [self._get_unique_variants(word.syllable_variants)
                    for word in self.line_chain_of_words]
        else:
            return [word.syllable_variants[0] for word in self.line_chain_of_words]
        
    @property
    def line_chain_of_words(self) -> list[Word]:
        words_in_line = self.text.split()
        result = []
    
        for word in words_in_line:
            if "-" in word:
                # Split compound words on dashes
                parts = word.split("-")
                result.extend([Word(text=part) for part in parts])
            else:
                result.append(Word(text=word))
    
        return result

    @staticmethod
    def _get_unique_variants(variants: list[int]) -> list[int]:
        """Remove duplicate syllable counts while preserving order."""
        seen = set()
        unique = []
        for variant in variants:
            if variant not in seen:
                seen.add(variant)
                unique.append(variant)
        return unique


@dataclass
class Stanza:
    lines: list[Line]

    def __post_init__(self) -> None:
        if not self.lines:
            raise ValueError("Stanza must contain at least one Line")
    
    @property
    def stanza_text_string(self) -> str:
        return '\n'.join(line.text for line in self.lines)