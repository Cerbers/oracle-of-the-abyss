"""Syllable counting module using the CMU Pronouncing Dictionary.

This module provides functionality to count syllables in English words
using the CMU Pronouncing Dictionary for accurate phonetic-based counting,
with fallback heuristics for words not in the dictionary.
"""

from nltk.corpus import cmudict

try:
    d = cmudict.dict()
except LookupError:
    raise RuntimeError(
        "CMUdict not found. Install it with: python -m nltk.downloader cmudict"
    ) from None

# TODO increase accuracy of count_syllables by adding more rules

vowels = "aeiouy"


def count_phonetically(word: str) -> int:
    """Count syllables using the CMU Pronouncing Dictionary.

    Looks up the word in the CMU dictionary and counts stress markers
    (digits 0, 1, 2) which indicate syllable nuclei.

    Args:
        word: The word to count syllables for. Must exist in the CMU dictionary.

    Returns:
        The number of syllables in the word based on phonetic transcription.

    Raises:
        KeyError: If the word is not found in the CMU dictionary.

    Example:
        >>> count_phonetically("hello")
        2
    """
    return len([ph for ph in d[word][0] if ph[-1].isdigit()])


def count_syllables(word: str) -> int:
    """Count syllables in a word with multiple fallback strategies.

    Attempts to count syllables using these methods in order:
    1. Direct lookup in CMU dictionary
    2. Lowercase lookup in CMU dictionary
    3. Elision detection (e.g., "o'er" -> 1 syllable instead of 2)
    4. Stripped punctuation lookup in CMU dictionary
    5. Vowel group counting as final fallback

    Args:
        word: The word to count syllables for.

    Returns:
        The estimated number of syllables in the word.

    Example:
        >>> count_syllables("rhythm")
        2
        >>> count_syllables("o'er")
        1
    """
    if word in d:
        return count_phonetically(word)
    word_lower = word.lower()

    if word_lower in d:
        return count_phonetically(word_lower)

    if "'" in word_lower:
        before, sep, after = word_lower.partition("'")
        if before and after and any(v in vowels for v in before[-1:]) \
            and any(v in vowels for v in after[:1]):
            # it is a real elision -> fallback and subtract 1
            return fallback_estimate(word_lower) - 1

    word_stripped = word_lower.strip(".,;:!?\"'()[]{}")

    if word_stripped in d:
        return count_phonetically(word_stripped)
    else:
        return fallback_estimate(word_stripped)


def fallback_estimate(word: str) -> int:
    """Estimate syllable count using vowel group heuristics.

    Counts groups of consecutive vowels as syllables. This is a
    simple heuristic that works for many English words but may
    be inaccurate for words with silent vowels or unusual spelling.

    Args:
        word: The word to estimate syllables for.

    Returns:
        The estimated number of syllables based on vowel groups.

    Example:
        >>> fallback_estimate("beautiful")
        4
        >>> fallback_estimate("rhythm")
        1  # Inaccurate, but expected fallback behavior
    """
    count = 0
    in_vowel = False

    for char in word:
        if char in vowels:
            if not in_vowel:
                count += 1
                in_vowel = True
        else:
            in_vowel = False

    return count
