from oracle.syllable_counter import count_phonetically, fallback_estimate, count_syllables

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