from oracle.syllable_counter import count_phonetically, fallback_estimate, count_syllables


def test_count_phonetically():
    """Test the phonetic syllable counting function using CMU Pronouncing Dictionary."""
    
    test_cases = {
        "hello": [2, 2], # multiple pronunciations but same syllable count
        "world": [1],
        "syllable": [3],
        "test": [1],
        "fire": [2, 1],  # multiple pronunciations
        "our": [2, 1, 1]    # multiple pronunciations
    }
    for word, expected_counts in test_cases.items():
        assert count_phonetically(word) == expected_counts


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

def test_count_syllables(): #needs updating
    """Test the syllable counting function for individual words."""
    # right now it only returns one int, but it should return list[int] of all variants instead
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
        assert count_syllables(word)[0] == expected_count