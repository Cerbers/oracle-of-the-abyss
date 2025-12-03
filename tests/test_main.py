from oracle.poem_model import Poem
from oracle.main import read_poem_file_and_return_content, write_poem_analysis, read_poem_folder_and_return_names, \
read_multiple_poem_files_and_write_analyses
from pathlib import Path

# TODO add test for error handling in read_poem_file_and_return_content

def test_read_poem_folder_and_return_names_excludes_analysis_files():
    """Test that analysis files are excluded when reading poem folder."""

    test_case_folder = read_poem_folder_and_return_names("user poems")

    assert all(not name.endswith("_analysis.txt") for name in test_case_folder), \
    "read_poem_folder_and_return_names should exclude analysis files."

def test_read_poem_folder_and_return_names():
    """Test reading all poems from a folder."""

    test_case_folder = read_poem_folder_and_return_names("user poems")

    assert isinstance(test_case_folder, list), "read_poem_folder_and_return_names should return a list."
    assert "The Serpent_analysis.txt" not in test_case_folder, \
    "read_poem_folder_and_return_names should not include analysis files."

def test_read_poem_file_and_return_content(capsys):
    """Test reading a poem from a text file."""

    test_poem_file = Path(__file__).parent.parent / "user poems" / "The Serpent.txt"
    assert test_poem_file.exists(), "Test poem file does not exist."
    
    poem_content = read_poem_file_and_return_content(str(test_poem_file))
    captured = capsys.readouterr()
    assert poem_content != "", "Failed to read the poem content."

def test_write_poem_analysis(tmp_path):
    poem_content = '''"Voidborn"
Born out of the void
Amidst the stars of flesh'''

    poem_file = tmp_path / "Voidborn.txt"
    poem_file.write_text(poem_content)

    write_poem_analysis(str(poem_file))

    analysis_file = tmp_path / "Voidborn_analysis.txt"
    assert analysis_file.exists()

    analysis_text = analysis_file.read_text()
    # Check for formatted stanza output
    assert "Stanza 1:" in analysis_text
    assert "Born out of the void" in analysis_text
    assert "Lines: 2" in analysis_text
    assert "Syllables per line:" in analysis_text


def test_poem_files_are_not_empty():
    """Test that when read_poem_folder_and_return_names is called empty files are not included."""

    poem_file_names = read_poem_folder_and_return_names("user poems")

    for poem_file_name in poem_file_names:
        poem_file_path = Path("user poems") / poem_file_name
        poem_content = read_poem_file_and_return_content(str(poem_file_path))
        assert poem_content.strip() != "", f"Poem file {poem_file_name} is empty."

def test_read_multiple_poem_files_and_write_analyses(tmp_path, monkeypatch):
    """Test reading multiple poem files and writing their analyses."""

    read_multiple_poem_files_and_write_analyses()

    test_poems = {
        "poem1.txt": """First line
Second line

Third line""",
        "poem2.txt": """Single stanza poem
With two lines""",
        "poem3.txt": """Another poem
Multiple lines
In one stanza"""
    }

    for filename, content in test_poems.items():
        poem_file = tmp_path / filename
        poem_file.write_text(content)

        def mock_read_poem_folder_and_return_names(folder_path: str) -> list[str]:
            poem_texts = []
            folder = Path(folder_path)

            for file_path in folder.glob("*.txt"):
                if not file_path.name.endswith("_analysis.txt"):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        if file.read().strip() != "":
                            poem_texts.append(file_path.name)
            return poem_texts
        

    def mock_read_multiple():
        poem_file_names = mock_read_poem_folder_and_return_names(str(tmp_path))

        for poem_file_name in poem_file_names:
            poem_file_path = tmp_path / poem_file_name
            write_poem_analysis(str(poem_file_path))
            
    mock_read_multiple()

    analysis_files = list(tmp_path.glob("*_analysis.txt"))
    poem_files = [f for f in tmp_path.glob("*.txt") if not f.name.endswith("_analysis.txt")]

    assert len(analysis_files) == len(test_poems), f"Excepted {len(test_poems)} analysis files, found {len(analysis_files)}."

    assert len(poem_files) == len(test_poems), f"Expected {len(test_poems)} poem files, found {len(poem_files)}."

    for poem_file in poem_files:
        analysis_file = tmp_path / (poem_file.stem + "_analysis.txt")
        assert analysis_file.exists(), f"Analysis file for {poem_file.name} does not exist."

        assert analysis_file.read_text().strip() != "", f"Analysis file for {poem_file.name} is empty."

def test_read_multiple_poem_files_with_empty_folder(tmp_path, monkeypatch):
    """Test that function handles empty folder gracefully."""
    
    monkeypatch.chdir(tmp_path)
    empty_folder = tmp_path / "user poems"
    empty_folder.mkdir()
    
    # Should not crash
    read_multiple_poem_files_and_write_analyses()
    
    # No analysis files should be created
    analysis_files = list(empty_folder.glob("*_analysis.txt"))
    assert len(analysis_files) == 0, "No analysis files should be created for empty folder"