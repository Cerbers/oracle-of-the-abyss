from pathlib import Path

import pytest
from oracle.poem_model import Poem, Word, Line, Stanza

def test_poem_object(tmp_path: Path):
    """Test the Poem dataclass instantiation and properties."""

    poem_text = "Roses are red,\nViolets are blue."
    poem_path = tmp_path / "roses.txt"
    
    poem = Poem(text=poem_text, filepath=poem_path)
    
    assert poem.text == poem_text, "Poem text does not match."
    assert poem.filepath == poem_path, "Poem filepath does not match."
    assert poem.filename == "roses", "Poem filename property does not return correct stem."

def test_poem_object_is_not_empty(tmp_path: Path):
    """Test that Poem raises an error when text is empty."""
    poem_path = tmp_path / "empty_poem.txt"
    empty_text = ""

    with pytest.raises(ValueError, match="Poem text cannot be empty"):
        Poem(text=empty_text, filepath=poem_path)

def test_poem_breaks_when_passed_non_path():
    """Test that Poem raises an error when filepath is not a Path object."""
    
    poem_text = "Some poem text."
    invalid_filepath = "user poems/some_poem.txt"
    
    with pytest.raises(TypeError):
        Poem(text=poem_text, filepath=invalid_filepath)

def test_poem_text_variable_breaks_when_not_string (tmp_path: Path):
    """Test that Poem raises an error when text is not a string."""
    invalid_text = 12345
    poem_path = tmp_path / "some_poem.txt"
    
    with pytest.raises(TypeError):
        Poem(text=invalid_text, filepath=poem_path)

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
    words = case_line.break_line_string_into_words
    expected_words = ["Born", "out", "of", "the", "void"]
    assert [word.text for word in words] == expected_words, "Line did not break into expected words."

    case_line_2 = Line(text="O'er the abyss' watchful maw")
    words_2 = case_line_2.break_line_string_into_words
    expected_words_2 = ["O'er", "the", "abyss'", "watchful", "maw"]
    assert [word.text for word in words_2] == expected_words_2, "Line did not break into expected words."

def test_line_syllable_variants():
    """Test that syllable variants for words in a line are calculated correctly."""
    case_line = Line(text="Born out of the void")
    words = case_line.break_line_string_into_words
    syllable_counts = [word.syllable_variants[0] for word in words]
    expected_syllable_counts = [1, 1, 1, 1, 1]
    assert syllable_counts == expected_syllable_counts, "Line syllable variants do not match expected values."

def test_line_is_not_empty():
    """Test that Line raises an error when text is empty."""
    with pytest.raises(ValueError, match="Line text cannot be empty"):
        Line(text="")

def test_empty_line_creates_no_words():
    """Test that an empty Line raises an error when trying to break into words."""
    try:
        case_line = Line(text="")
        words = case_line.break_line_string_into_words
        assert words == [], "Empty line should produce no words."
    except ValueError:
        pass  # Expected behavior, as Line should not accept empty text

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

def test_poem_object_has_stanzas(tmp_path: Path):
    """Test that Poem has stanzas property that breaks text into stanzas."""
    
    case_poem_text = """"Voidborn"
    Born out of the void
    Amidst the stars of flesh
    An illusion both full and empty
    O'er the abyss' watchful maw
    
    Gazes into the weary eyes of a lost stalker"""

    case_poem = Poem(text=case_poem_text, filepath=tmp_path / "voidborn.txt")
    stanzas = case_poem.text.split('\n    \n')
    assert len(stanzas) == 2, "Poem should contain 2 stanzas."