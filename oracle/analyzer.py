from nltk.corpus import cmudict

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

def analyze_poem(poem_text: str) -> dict[str, str | int | list[int]]:
    """Analyzes a poem - syllables per line, total lines"""

    blank_lines_removed = []
    for line in poem_text.split('\n'):
        if line.strip():
            blank_lines_removed.append(line)
    syllables_per_line = [count_syllables_in_line(line) for line in blank_lines_removed]

    return {
        'poem': poem_text,
        'Lines': len(blank_lines_removed),
        'Syllables_per_line': syllables_per_line
    }