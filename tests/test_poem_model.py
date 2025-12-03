from pathlib import Path

import pytest
from oracle.domain_objects import Line, Stanza
from oracle.poem_model import Poem

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



def test_poem_object_has_stanzas(tmp_path: Path):
    """Test that Poem has stanzas property that breaks text into stanzas."""
    
    case_poem_text = """"Voidborn"
    Born out of the void
    Amidst the stars of flesh
    An illusion both full and empty
    O'er the abyss' watchful maw
    
    Gazes into the weary eyes of a lost stalker"""

    case_poem = Poem(text=case_poem_text, filepath=tmp_path / "voidborn.txt")
    stanzas = case_poem.stanzas

    # structural assertions
    assert len(stanzas) == 2, "Poem should contain 2 stanzas."
    assert isinstance(stanzas, list), "Poem stanzas should be a list."
    assert all(isinstance(stanza, Stanza) for stanza in stanzas), "Each stanza should be a Stanza object."
    assert all(isinstance(line, Line) for stanza in stanzas for line in stanza.lines), "Each line should be a Line object."

    # content assertions
    assert stanzas[0].lines[0].text == "Born out of the void", "First line of first stanza is incorrect."
    assert len(stanzas[0].lines) == 4, "First stanza should have 4 lines."
    assert len(stanzas[1].lines) == 1, "Second stanza should have 1 line."
