from pathlib import Path
from oracle.poem_model import Poem
from oracle.analyzer import analyze_poem, check_for_title_line


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

    poem_with_title_1 = """"Voidborn"
    Born out of the void
    Amidst the stars of flesh"""

    poem_with_title_2 = """ "Voidborn" 
    Born out of the void
    Amidst the stars of flesh"""

    poem_with_title_3 = """ VOIDBORN
    Born out of the void
    Amidst the stars of flesh"""

    # Fake filepath for filename matching
    poem_obj = Poem(text="", filepath=Path("Voidborn.txt"))

    first_line_1 = poem_with_title_1.split("\n")[0]
    first_line_2 = poem_with_title_2.split("\n")[0]
    first_line_3 = poem_with_title_3.split("\n")[0]

    assert check_for_title_line(first_line_1, poem_obj)
    assert check_for_title_line(first_line_2, poem_obj)
    assert check_for_title_line(first_line_3, poem_obj)