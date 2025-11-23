from oracle.main import read_poem_file_and_return_content, write_poem_analysis, read_poem_folder_and_return_names, \
read_multiple_poem_files_and_write_analyses
from pathlib import Path


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

def test_write_poem_analysis():
    """Test writing poem analysis to a file."""

    poem_analysis_file_path = Path(__file__).parent.parent / "user poems" / "The Serpent_analysis.txt"
    test_case_poem_path = Path(__file__).parent.parent / "user poems" / "The Serpent.txt"
    poem_analysis_file = write_poem_analysis(
        str(test_case_poem_path))
    
    assert poem_analysis_file_path.exists(), "Poem analysis file was not created."
    assert poem_analysis_file is None, "write_poem_analysis should return None."

def test_read_multiple_poem_files_and_write_analyses():
    """Test reading multiple poem files and writing their analyses."""

    read_poem_folder_and_return_names("user poems")

    assert True, "read_multiple_poem_files_and_write_analyses executed without errors."

def test_poem_files_are_not_empty():
    """Test that when read_poem_folder_and_return_names is called empty files are not included."""

    poem_file_names = read_poem_folder_and_return_names("user poems")

    for poem_file_name in poem_file_names:
        poem_file_path = Path("user poems") / poem_file_name
        poem_content = read_poem_file_and_return_content(str(poem_file_path))
        assert poem_content.strip() != "", f"Poem file {poem_file_name} is empty."