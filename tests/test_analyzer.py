from oracle.analyzer import analyze_poem, count_syllables

def test_poem_analyzer():
    """Test the poem analyzer function, 
    checking syllable counts per line and total lines."""

    poem = """ Born out of the void
    Amidst the stars of flesh
    An illusion both full and empty
    O'er the abyss' watchful maw"""

    analysis = analyze_poem(poem)
    expected = {'Lines': 4, 'Syllables_per_line': [5,6,9,7]}
    assert analysis == expected


def test_syllable_counter():
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