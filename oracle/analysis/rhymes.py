"""
Rhyme detection module.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from oracle.domain_objects import Word

if TYPE_CHECKING:
    from oracle.domain_objects import Stanza


def _rhyme_sound(word_text: str) -> str:
    """
    Extract the rhyme sound for a word.

    Uses CMU phonemes when available: returns the phoneme sequence from the
    last stressed vowel (phoneme ending in '1' or '2') to the end of the
    first pronunciation.  Falls back to the last two characters of the
    stripped, lowercased word.
    """
    
    word = Word(text=word_text)
    pronunciations = word.phonemes
    if pronunciations:
        phones = pronunciations[0]
        for i in range(len(phones) - 1, -1, -1):
            if phones[i][-1] in ('1', '2'):
                return ' '.join(phones[i:])
    # fallback: last two characters
    stripped = word_text.lower().strip('.,!?":;\'')
    return stripped[-2:] if len(stripped) >= 2 else stripped

# TODO: Add reliable, flexible support for more complex rhyme patterns
def _name_scheme(pattern: str) -> str:
    """"""
    if len(set(pattern)) == 1:
        return "Monorhyme"
    if pattern in "AABBCCDDEEFFGG":
        return "Rhyming Couplets"
    if pattern in "ABABABABABABABAB":
        return "Alternating Rhyme"
    if pattern == "ABBA":
        return "Enclosed Rhyme"
    elif pattern == pattern[::-1]:
        return "Mirrored Rhyme" # Technically it's 'Enclosed Rhyme' but for clarity and personal preference
                                # We're going to call it 'Mirrored Rhyme' leaving ER for 4 line stanza pattern
    return "No recognized rhyme pattern"


def detect_rhymes(poem_stanza: Stanza) -> list[str]:
    """
    Detect the rhyme scheme of a stanza.

    Returns:
        A list of one or two strings:
          - [pattern]              e.g. ["ABCD"]    
          - [pattern, name]        e.g. ["AABB", "Rhyming Couplets"]
        Returns [] for stanzas with fewer than 2 lines.
    """
    if len(poem_stanza.lines) < 2:
        return []

    # Get rhyme sound for the last word of each line
    sounds: list[str] = []
    for line in poem_stanza.lines:
        words = line.line_chain_of_words
        last_word_text = words[-1].text if words else ""
        sounds.append(_rhyme_sound(last_word_text))

    # Assign letters to unique sounds in order of first appearance
    sound_to_letter: dict[str, str] = {}
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for sound in sounds:
        if sound not in sound_to_letter:
            sound_to_letter[sound] = LETTERS[len(sound_to_letter)]

    pattern = ''.join(sound_to_letter[s] for s in sounds)
    name = _name_scheme(pattern)

    return [pattern, name] if name else [pattern]