from pathlib import Path
from oracle.poem_model import Poem
from oracle.analyzer import analyze_poem, check_for_title_line, parse_into_stanzas


# TODO expand test cases for edge cases


def test_analyze_poem():
    """Test the poem analyzer function, 
    checking syllable counts per line and total lines."""

    poem = """"Voidborn"
    Born out of the void
    Amidst the stars of flesh
    An illusion both full and empty
    O'er the abyss' watchful maw
    
    Gazes into the weary eyes of a lost stalker"""
    poem_obj = Poem(text=poem, filepath=Path("test_poem.txt"))
    analysis = analyze_poem(poem_obj)
    expected = {'poem': poem,'Lines': 5, 'Syllables_per_line': [5,6,9,7,13]}
    assert analysis == expected



def test_check_for_title_line():
    """Test that title lines are correctly identified and skipped in poem analysis."""

    # Fake filepath for filename matching
    poem_obj = Poem(text="filler", filepath=Path("Voidborn.txt"))

    test_cases = [
        'Voidborn',
        '"Voidborn"',
        'VOIDBORN',
        "'Voidborn'"
    ]

    for line in test_cases:
        assert check_for_title_line(line, poem_obj) is True, f"Failed to identify title line: {line}"


def test_parse_into_stanzas():
    """Test that poem text is correctly parsed into stanzas (lists of line lists).
    Stanzas are separated by blank lines where blank line/s count in between is n >=1."""

    case_poem_texts = {
        "Case 1": """"Voidborn"
    Born out of the void
    Amidst the stars of flesh
    An illusion both full and empty
    O'er the abyss' watchful maw
    
    Gazes into the weary eyes of a lost stalker""",
        "Case 2": """"Voidborn"
    Born out of the void
    Amidst the stars of flesh
    An illusion both full and empty
    O'er the abyss' watchful maw
    

    Gazes into the weary eyes of a lost stalker"""
    }
    
    for case_name, poem_text in case_poem_texts.items():
        stanzas = parse_into_stanzas(poem_text)
        assert len(stanzas) == 2, f"{case_name} failed to parse into 2 stanzas."
        assert all(isinstance(stanza, list) for stanza in stanzas), f"{case_name} stanzas are not lists."
        assert all(all(isinstance(line, str) for line in stanza) for stanza in stanzas), f"{case_name} lines are not strings."