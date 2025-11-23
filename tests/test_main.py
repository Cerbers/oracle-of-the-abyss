from oracle.main import read_poem_file
from pathlib import Path


def test_read_poem_file(capsys):
    """Test reading a poem from a text file."""

    test_poem_file = Path(__file__).parent.parent / "user poems" / "The Serpent.txt"
    assert test_poem_file.exists(), "Test poem file does not exist."
    
    poem_content = read_poem_file(str(test_poem_file))
    captured = capsys.readouterr()
    assert poem_content != "", "Failed to read the poem content."

