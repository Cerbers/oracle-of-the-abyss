from pathlib import Path

import pytest
from oracle.poem_model import Poem

def test_poem_object():
    """Test the Poem dataclass instantiation and properties."""
    poem_text = "Roses are red,\nViolets are blue."
    poem_path = Path("user poems/roses.txt")
    
    poem = Poem(text=poem_text, filepath=poem_path)
    
    assert poem.text == poem_text, "Poem text does not match."
    assert poem.filepath == poem_path, "Poem filepath does not match."
    assert poem.filename == "roses", "Poem filename property does not return correct stem."

def test_poem_breaks_when_passed_non_path():
    """Test that Poem raises an error when filepath is not a Path object."""
    poem_text = "Some poem text."
    invalid_filepath = "user poems/some_poem.txt"
    
    with pytest.raises(TypeError):
        Poem(text=poem_text, filepath=invalid_filepath)

def test_poem_text_variable_breaks_when_not_string():
    """Test that Poem raises an error when text is not a string."""
    invalid_text = 12345
    poem_path = Path("user poems/some_poem.txt")
    
    with pytest.raises(TypeError):
        Poem(text=invalid_text, filepath=poem_path)