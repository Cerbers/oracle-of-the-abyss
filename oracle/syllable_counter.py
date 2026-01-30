"""
Syllable counting module for the Oracle Poetry Analyzer.
"""

import nltk # type: ignore[import-untyped]
from nltk.corpus import cmudict # type: ignore[import-untyped]


try:
    DICTIONARY_CMUDICT = cmudict.dict()
except LookupError:
    nltk.download('cmudict', quiet=True)
    DICTIONARY_CMUDICT = cmudict.dict()

# TODO increase accuracy of count_syllables by adding more rules
VOWELS = "aeiouy"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
LETTERS = VOWELS + CONSONANTS


def count_phonetically(word: str) -> list[int]:
    """
    Count syllables in a word using CMU Pronouncing Dictionary.
    
    Args:
        word: The word to count syllables for.
    
    Returns:
        A list of possible syllable counts for the word object.
    """

    syllable_counts = []
    for pronunciation in DICTIONARY_CMUDICT[word]:
        syllable_count = len([phoneme for phoneme in pronunciation if phoneme[-1].isdigit()])
        syllable_counts.append(syllable_count)
    
    return syllable_counts

def count_syllables(word: str) -> list[int]:
    """
    Count syllables in a word using CMU dictionary and fallback methods.

    Args:
        word: The word to count syllables for.

    Returns:
        A list of possible syllable counts for the word object.

    Note:
        Returns a list because some words have multiple pronunciations.
    """
    # case sensitive check, in case CMU has the word with different capitalization
    if word in DICTIONARY_CMUDICT:
        return count_phonetically(word)
    word_lower = word.lower()

    if word_lower in DICTIONARY_CMUDICT:
        return count_phonetically(word_lower)
    
    if "'" in word_lower:
        before, sep, after = word_lower.partition("'")
        if before and after and any(v in VOWELS for v in before[-1:]) \
            and any(v in VOWELS for v in after[:1]):
            # it is a real elision -> fallback and subtract 1
            return [fallback_estimate(word_lower) - 1]
    
    word_stripped = word_lower.strip(".,;:!?\"'()[]{}#*_")

    if word_stripped in DICTIONARY_CMUDICT:
        return count_phonetically(word_stripped)
    else:
        return [fallback_estimate(word_stripped)]

def fallback_estimate(word: str) -> int:
    """
    A simple syllable counting function based on vowel groups.
    
    Args:
        word: The word to count syllables for.
    
    Returns:
        The estimated number of syllables in the word.
    """

    count = 0
    in_vowel = False

    for char in word:
        if char in VOWELS:
            if not in_vowel:
                count += 1
                in_vowel = True
        else:
            in_vowel = False

    return count
