import nltk # type: ignore[import-untyped]
from nltk.corpus import cmudict # type: ignore[import-untyped]


try:
    DICTIONARY_CMUDICT = cmudict.dict()
except LookupError:
    nltk.download('cmudict', quiet=True)
    DICTIONARY_CMUDICT = cmudict.dict()

# TODO increase accuracy of count_syllables by adding more rules
# TODO: make count_syllables return list[int] of all variants instead of just one int once syllable_pattern is fully functional
VOWELS = "aeiouy"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
LETTERS = VOWELS + CONSONANTS


def count_phonetically(word: str) -> list[int]:
    """"Count syllables in a word using CMU Pronouncing Dictionary."""
    syllable_counts = []
    for pronunciation in DICTIONARY_CMUDICT[word]:
        syllable_count = len([phoneme for phoneme in pronunciation if phoneme[-1].isdigit()])
        syllable_counts.append(syllable_count)
    
    return syllable_counts

def count_syllables(word: str) -> list[int]:
    """Count syllables in a word using CMU Pronouncing Dictionary, 
    lowercase fallback, elision handling, and stripping punctuation.
    If all else fails, use a simple vowel counting method."""

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
    """A simple syllable counting function based on vowel groups."""

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
