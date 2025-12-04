from nltk.corpus import cmudict # type: ignore[import-untyped]
try:
    DICTIONARY_CMUDICT = cmudict.dict()
except LookupError:
    raise RuntimeError(
        "CMUdict not found. Install it with: python -m nltk.downloader cmudict"
    ) from None

# TODO increase accuracy of count_syllables by adding more rules
# TODO: make count_syllables return list[int] of all variants instead of just one int
# TODO: make count_phonetically return list of unique syllable counts instead of all variants
vowels = "aeiouy"

def count_phonetically(word: str) -> list[int]:
    """"Count syllables in a word using CMU Pronouncing Dictionary."""
    return [len([ph for ph in pron if ph[-1].isdigit()]) for pron in DICTIONARY_CMUDICT[word]]



def count_syllables(word: str) -> list[int]:
    """Count syllables in a word using CMU Pronouncing Dictionary, 
    lowercase fallback, elision handling, and stripping punctuation.
    If all else fails, use a simple vowel counting method."""

    if word in DICTIONARY_CMUDICT:
        return [count_phonetically(word)][0]
    word_lower = word.lower()

    if word_lower in DICTIONARY_CMUDICT:
        return [count_phonetically(word_lower)][0]
    
    if "'" in word_lower:
        before, sep, after = word_lower.partition("'")
        if before and after and any(v in vowels for v in before[-1:]) \
            and any(v in vowels for v in after[:1]):
            # it is a real elision -> fallback and subtract 1
            return [fallback_estimate(word_lower) - 1]
    
    word_stripped = word_lower.strip(".,;:!?\"'()[]{}")

    if word_stripped in DICTIONARY_CMUDICT:
        return [count_phonetically(word_stripped)][0]
    else:
        return [fallback_estimate(word_stripped)]

def fallback_estimate(word: str) -> int:
    """A simple syllable counting function based on vowel groups."""

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
