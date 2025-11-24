from pathlib import Path
from oracle.poem_model import Poem
from oracle.analyzer import analyze_poem, count_syllables, count_phonetically, fallback_estimate, count_syllables_in_line, \
    check_for_title_line



# TODO expand test cases for edge cases
# TODO remake test_count_phonetically to separate tests for words in CMU and not in CMU

def test_count_phonetically():
    """Test the phonetic syllable counting function using CMU Pronouncing Dictionary."""

    not_cmu_word_count = 0
    in_cmu_word_count = 0
    test_cases = {
        "illusion": 3,
        "abyss": 2,
        "flesh": 1,
        "o'er": 1,
        "watchful": 2,
        "maw": 1,
        "make": 1
    }
    for word, expected_count in test_cases.items():
        print(f"Testing phonetic count for word: {word}")
        try:
            assert count_phonetically(word) == expected_count
            in_cmu_word_count += 1
        except KeyError:
            not_cmu_word_count += 1
            
    assert not_cmu_word_count == 1
    assert in_cmu_word_count == len(test_cases) - 1


def test_fallback_estimate():
    """Test the fallback syllable counting function based on vowel groups."""
    test_cases = {
        "illusion": 3,
        "abyss": 2,
        "flesh": 1,
        "o'er": 2,
        "watchful": 2,
        "maw": 1,
        "rhythm": 1 # testing behavior if CMU fails, should return 1 even though it's 2 syllables
    }
    for word, expected_count in test_cases.items():
        assert fallback_estimate(word) == expected_count



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


def test_count_syllables():
    """Test the syllable counting function for individual words."""

    test_cases = {
        "illusion": 3,
        "abyss'": 2,
        "flesh": 1,
        "o'er": 1,
        "watchful": 2,
        "maw": 1,
        "you're": 1,
        "make": 1,
        "sheltered": 2,
        "rhythm": 2,
        "jumped": 1
    }
    for word, expected_count in test_cases.items():
        print(f"Testing word: {word}")
        assert count_syllables(word) == expected_count


def test_count_syllables_in_line():
    """Test the syllable counting function for a line of text."""

    line_1 = "O'er the abyss' watchful maw"
    expected_count_1 = 7
    line_2 = "Born out of the void"
    expected_count_2 = 5
    assert count_syllables_in_line(line_1) == expected_count_1
    assert count_syllables_in_line(line_2) == expected_count_2


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