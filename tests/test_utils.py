from pathlib import Path
from oracle.poem_model import Poem
from oracle.utils import check_for_title_line

def test_check_for_title_line():
    """Test that title lines are correctly identified and skipped in poem analysis."""

    # Fake filepath for filename matching
    poem_obj = Poem(text="filler", filepath=Path("Voidborn.txt"))

    test_cases = [
        'Voidborn',
        '"Voidborn"',
        'VOIDBORN',
        "'Voidborn'"
    ]

    for line in test_cases:
        assert check_for_title_line(line, poem_obj.filename) is True, f"Failed to identify title line: {line}"
