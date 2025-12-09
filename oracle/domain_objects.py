from dataclasses import dataclass
from oracle.syllable_counter import count_syllables


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
        
    def get_total_syllables(self, use_all_variants: bool = False) -> int | list[list[int]]:
        """
        Calculate total syllables for the line.

        Args:
            use_all_variants: If False (default), returns sum of first variants.
                             If True, returns nested list for pattern analysis.

        Returns:
            When False: 5 (sum of first variants)
            When True: [[2,1], [2,1]] (unique variants per word)
        """
        if use_all_variants:
            return self.get_syllable_counts(use_all_variants=True)
        else:
            return sum(self.get_syllable_counts(use_all_variants=False))

    @property
    def line_chain_of_words(self) -> list[Word]:
        words_in_line = self.text.split()
        return [Word(text=word) for word in words_in_line]

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