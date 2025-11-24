from nltk.corpus import cmudict
from oracle.poem_model import Poem

# TODO find a way to not count title if poem has one in the text file
# TODO have line count and syllable count show at end of each stanza
# TODO have total line count at the bottom of analysis text

d = cmudict.dict()
vowels = "aeiouy"

def count_phonetically(word: str) -> int:
    """"Count syllables in a word using CMU Pronouncing Dictionary."""
    return len([ph for ph in d[word][0] if ph[-1].isdigit()])



def count_syllables(word: str) -> int:
    """Count syllables in a word using CMU Pronouncing Dictionary, 
    lowercase fallback, elision handling, and stripping punctuation.
    If all else fails, use a simple vowel counting method."""

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

def count_syllables_in_line(line: str) -> int:
    """Count syllables in a line of text"""

    words = line.split()
    return sum(count_syllables(word) for word in words)

def analyze_poem(poem: Poem) -> dict:
    lines_with_text = []
    for line in poem.text.split('\n'):
        if check_for_title_line(line, poem):
            continue
        if line.strip():
            lines_with_text.append(line)

    syllables_per_line = [count_syllables_in_line(line) for line in lines_with_text]

    return {
        "poem": poem.text,
        "Lines": len(lines_with_text),
        "Syllables_per_line": syllables_per_line
    }

def check_for_title_line(line: str, poem: Poem) -> bool:
    """Check if the poem has a title line enclosed in quotes, all caps, 
    or if the first line is significantly shorter than the rest and coincides with file name."""

    stripped = line.strip()

    if stripped.startswith('"') and stripped.endswith('"'):
        return True

    if stripped.isupper():
        return True

    if stripped == poem.filename:
        return True

    return False