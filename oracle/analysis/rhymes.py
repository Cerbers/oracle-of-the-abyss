"""
Rhyme detection module.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from oracle.domain_objects import Word

if TYPE_CHECKING:
    from oracle.domain_objects import Stanza

def detect_rhymes(poem_stanza: Stanza) -> list[str]:
    """
    Detect the rhyme scheme of a stanza.

    Args:
        poem_stanza: The stanza to analyze.

    Returns:
        A list of one or two strings:
          - [pattern]              e.g. ["ABCD"]    
          - [pattern, name]        e.g. ["AABB", "Rhyming Couplets"]
        Returns empty list for stanzas with fewer than 2 lines.
    """
    if len(poem_stanza.lines) < 2:
        return []

    # Get rhyme sound for the last word of each line
    sounds: list[str] = []
    for line in poem_stanza.lines:
        words = line.line_chain_of_words
        # print(f"Words: {words}")
        last_word_text = words[-1].text if words else ""
        # print(f"Last word text: {last_word_text}")
        sounds.append(_rhyme_sound(last_word_text))

    # Assign letters to unique sounds in order of first appearance
    sound_to_letter: dict[str, str] = {}
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for sound in sounds:
        # print(f"Sound: {sound}")
        if sound not in sound_to_letter:
            sound_to_letter[sound] = LETTERS[len(sound_to_letter)]
            # print(f"Sound to letter: {sound_to_letter}")

    pattern = ''.join(sound_to_letter[s] for s in sounds)
    name = _name_scheme(pattern)

    return [pattern, name] if name else [pattern]



def _rhyme_sound(word_text: str) -> str:
    """
    Extract the rhyme sound for a word.

    Uses CMU phonemes when available: returns the phoneme sequence from the
    last stressed vowel (phoneme ending in '0', '1' or '2') to the end of the
    first pronunciation.  Falls back to the last two characters of the
    stripped, lowercased word.
    """
    
    word = Word(text=word_text)
    pronunciations = word.phonemes
    # print(f"Pronunciations: {pronunciations}")
    # print('-' * 80)
    if pronunciations:
        phones = pronunciations[0]
        # print(f"Phones: {phones}")
        for i in range(len(phones) - 1, -1, -1):
            if phones[i][-1] in ('0', '1', '2'):
                result = ' '.join(phones[i:])
                # print(f"Result: {result}")
                return result
    # fallback: last two characters
    stripped = word_text.lower().strip('.,!?":;\'')
    return stripped[-2:] if len(stripped) >= 2 else stripped


def _name_scheme(pattern: str) -> str:
    """Private function to check for specific rhyme patterns."""
    if len(set(pattern)) == 1:
        return "Monorhyme"

    repeating_unit = _find_repeating_unit(pattern)
    if repeating_unit is not None and repeating_unit != "Monorhyme":
        return "Alternating Rhyme"

    pairs = _check_for_pairs(pattern)
    if pairs is not None:
        return "Rhyming Couplets"

    if pattern == "ABBA":
        return "Enclosed Rhyme"
    elif pattern == pattern[::-1]:
        return "Mirrored Rhyme" # Technically it's 'Enclosed Rhyme' but for clarity and personal preference
                                # We're going to call it 'Mirrored Rhyme' leaving ER for classic 4 line stanza pattern

    return "No recognized rhyme pattern"


def _find_repeating_unit(pattern: str) -> str | None:
    """Private function to find repeating units in a pattern."""
    if pattern[0] == pattern[-1]:
        return "Monorhyme"

    n = len(pattern)
    for period in range(1, n // 2 + 1):
        if n % period != 0:
            continue # must divide evenly
        
        unit = pattern[:period]
        if unit * (n // period) == pattern:
            return unit
    return None # No repeating unit found

def _check_for_pairs(pattern: str) -> list[str] | None:
    """Private function to find pairs in a pattern."""
    if len(pattern) % 2 != 0:
        return None
    
    pairs = [pattern[i:i+2] for i in range(0, len(pattern), 2)]
    
    for p in pairs:
        if p[0] != p[1]:
            return None
    
    return pairs