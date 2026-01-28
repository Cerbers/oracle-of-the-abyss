import pytest

from oracle.domain_objects import Word, Line, Stanza

def test_word_object():
    """Test the Word dataclass instantiation and properties."""
    case_word = Word(text="example")
    assert case_word.text == "example", "Word text does not match."

def test_word_syllable_variants():
    """Test the syllable variants property of the Word dataclass."""
    case_word = Word(text="rhythm")
    assert case_word.syllable_variants == [2], "Word syllable variants do not match expected value."


def test_line_object():
    """Test the Line dataclass instantiation and properties."""
    case_line = Line(text="Born out of the void")
    assert case_line.text == "Born out of the void", "Line text does not match."


def test_line_breaks_line_string_into_words():
    """Test that Line breaks its text into Word objects correctly."""
    case_line = Line(text="Born out of the void")
    words = case_line.line_chain_of_words
    expected_words = ["Born", "out", "of", "the", "void"]
    assert [word.text for word in words] == expected_words, "Line did not break into expected words."

    case_line_2 = Line(text="O'er the abyss' watchful maw")
    words_2 = case_line_2.line_chain_of_words
    expected_words_2 = ["O'er", "the", "abyss'", "watchful", "maw"]
    assert [word.text for word in words_2] == expected_words_2, "Line did not break into expected words."

def test_line_syllable_variants():
    """Test that syllable variants for words in a line are calculated correctly."""
    case_line = Line(text="Born out of the void")
    words = case_line.line_chain_of_words
    syllable_counts = [word.syllable_variants[0] for word in words]
    expected_syllable_counts = [1, 1, 1, 1, 1]
    assert syllable_counts == expected_syllable_counts, "Line syllable variants do not match expected values."

def test_line_is_not_empty():
    """Test that Line raises an error when text is empty."""
    with pytest.raises(ValueError, match="Line text cannot be empty"):
        Line(text="")


def test_stanza_object():
    """Test the Stanza dataclass instantiation and properties."""
    case_stanza = Stanza(lines=[Line(text="Line one."), Line(text="Line two.")])

    assert len(case_stanza.lines) == 2, "Stanza does not contain the expected number of lines."
    assert case_stanza.lines[0].text == "Line one.", "First line text does not match."
    assert case_stanza.lines[1].text == "Line two.", "Second line text does not match."

def test_stanza_lines_are_line_objects():
    """Test that Stanza lines are instances of Line dataclass."""
    case_stanza = Stanza(lines=[Line(text="First line."), Line(text="Second line.")])

    for line in case_stanza.lines:
        assert isinstance(line, Line), "Stanza lines should be instances of Line dataclass."

def test_stanza_is_not_empty():
    """Test that Stanza can be instantiated with an empty list of lines."""
    with pytest.raises(ValueError, match="Stanza must contain at least one Line"):
        Stanza(lines=None)

def test_line_get_syllable_counts_returns_per_word_counts():
    """Test that the line count function returns the correct number of syllable in each word in a line."""
    
    case_line_1 = Line(text="Born out of the void")
    test_count_1 = case_line_1.get_syllable_counts()

    case_line_2 = Line(text="Who lies in blood-flow of the night")
    test_count_2 = case_line_2.get_syllable_counts()
    
    expected_syllable_counts_1 = [1, 1, 1, 1, 1]
    assert test_count_1 == expected_syllable_counts_1, "Line syllable variants do not match expected values."

    expected_syllable_counts_2 = [1, 1, 1, 1, 1, 1, 1, 1]
    assert test_count_2 == expected_syllable_counts_2, "Line syllable variants do not match expected values."

def test_stanza_has_text_representation_by_merging_lines():
    """Test that Stanza can merge its lines into a single text representation."""


    case_stanza_lines = Stanza(lines=[Line(text="First line."), Line(text="Second line.")])
    stanza_text = case_stanza_lines.stanza_text_string
    expected_text = "First line.\nSecond line."
    assert stanza_text == expected_text, "Stanza text representation does not match expected value."


def test_line_get_unique_variants():
    """Test that _get_unique_variants removes duplicates while preserving order."""
    line = Line(text="test")

    # Test with duplicates at end
    assert line._get_unique_variants([2, 1, 1]) == [2, 1]

    # Test with all duplicates
    assert line._get_unique_variants([2, 2]) == [2]

    # Test with single element
    assert line._get_unique_variants([1]) == [1]

    # Test with multiple duplicates scattered
    assert line._get_unique_variants([3, 2, 1, 2, 3]) == [3, 2, 1]


def test_line_get_syllable_counts_default_unchanged():
    """Test that default behavior returns first variant only (backwards compatible)."""
    case_line = Line(text="Born out of the void")
    counts = case_line.get_syllable_counts()

    # Should return first variant for each word
    assert counts == [1, 1, 1, 1, 1]
    assert isinstance(counts, list)
    assert all(isinstance(c, int) for c in counts)


def test_line_get_syllable_counts_all_variants():
    """Test that use_all_variants=True returns unique variants per word."""
    case_line = Line(text="fire our")
    counts = case_line.get_syllable_counts(use_all_variants=True)

    # fire=[2,1], our=[2,1,1]→[2,1] after deduplication
    assert counts == [[2, 1], [2, 1]]
    assert isinstance(counts, list)
    assert all(isinstance(c, list) for c in counts)


def test_line_get_total_syllables_default_unchanged():
    """Test that default behavior returns sum (backwards compatible)."""
    case_line = Line(text="Born out of the void")
    total = case_line.get_total_syllables()

    assert total == 5
    assert isinstance(total, int)


def test_line_get_all_syllable_variants():
    """Test that get_all_syllable_variants returns nested structure."""
    case_line = Line(text="fire our")
    variants = case_line.get_all_syllable_variants()

    # Should return the same structure as get_syllable_counts(use_all_variants=True)
    assert variants == [[2, 1], [2, 1]]
    assert isinstance(variants, list)
    assert all(isinstance(v, list) for v in variants)


def test_line_all_variants_edge_cases():
    """Test edge cases for all variants mode."""
    # Single word with variants
    case_line_single = Line(text="fire")
    variants_single = case_line_single.get_all_syllable_variants()
    assert variants_single == [[2, 1]]

    # All single-variant words should still return nested structure
    case_line_simple = Line(text="test")  # test=[1]
    variants_simple = case_line_simple.get_all_syllable_variants()
    assert variants_simple == [[1]]
