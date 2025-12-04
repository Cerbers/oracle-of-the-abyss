from oracle.syllable_pattern import pull_single_syllable_variant_from_words

def test_pull_single_syllable_variant_from_words():
    """Test pulling words with a single syllable variant."""

    words = ["hello", "world", "syllable", "test", 'fire', 'our'] # hello has 2 different pronunciations but same syllable count
    expected_single_syllable_variant = ["hello", "world", "syllable", "test"] # 'fire' and 'our' have multiple syllable variants

    single_syllable_variant = pull_single_syllable_variant_from_words(words)

    assert single_syllable_variant == expected_single_syllable_variant, \
    f"Expected {expected_single_syllable_variant}, but got {single_syllable_variant}."