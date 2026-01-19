from oracle.main import read_poem_file_and_return_content, write_poem_analysis, read_poem_folder_and_return_names, \
read_multiple_poem_files_and_write_analyses
from pathlib import Path

# TODO add test for error handling in read_poem_file_and_return_content

def test_read_poem_folder_and_return_names_excludes_analysis_files(tmp_path):
    """Test that analysis files are excluded when reading poem folder."""
    # Create poem files and analysis files
    (tmp_path / "poem1.txt").write_text("Some poem content")
    (tmp_path / "poem2.txt").write_text("Another poem")
    (tmp_path / "poem1_analysis.txt").write_text("Analysis of poem1")
    (tmp_path / "poem2_analysis.txt").write_text("Analysis of poem2")

    test_case_folder = read_poem_folder_and_return_names(str(tmp_path))

    assert all(not name.endswith("_analysis.txt") for name in test_case_folder), \
        "read_poem_folder_and_return_names should exclude analysis files."
    assert "poem1.txt" in test_case_folder
    assert "poem2.txt" in test_case_folder

def test_read_poem_folder_and_return_names(tmp_path):
    """Test reading all poems from a folder."""
    # Create some poem files
    (tmp_path / "poem1.txt").write_text("First poem")
    (tmp_path / "poem2.txt").write_text("Second poem")
    (tmp_path / "some_analysis.txt").write_text("Should be excluded")

    test_case_folder = read_poem_folder_and_return_names(str(tmp_path))

    assert isinstance(test_case_folder, list), "read_poem_folder_and_return_names should return a list."
    assert "some_analysis.txt" not in test_case_folder, \
        "read_poem_folder_and_return_names should not include analysis files."

def test_read_poem_file_and_return_content_from_real_example(capsys):
    """Test reading a poem from a text file (using real user poems folder)."""
    example_file = Path(__file__).parent.parent / "user poems" / "The Serpent.txt"
    assert example_file.exists(), f"Example file missing: {example_file}. Cannot test real-data path."

    poem_content = read_poem_file_and_return_content(str(example_file))
    captured = capsys.readouterr()
    assert poem_content.strip() != "", "Real example file should not be empty."

def test_read_poem_file_and_return_content_with_tmp_path(tmp_path):
    """Test reading a poem file with controlled test data using tmp_path."""
    poem_text = "Roses are red\nViolets are blue"
    poem_file = tmp_path / "test_poem.txt"
    poem_file.write_text(poem_text)

    poem_content = read_poem_file_and_return_content(str(poem_file))

    assert poem_content == poem_text, "Read content should match written content."

def test_read_poem_file_and_return_content_file_not_found(tmp_path: Path, capsys):
    non_existent = tmp_path / "missing.txt"
    poem_content = read_poem_file_and_return_content(str(non_existent))
    captured = capsys.readouterr()
    assert poem_content == "", "Should return empty on missing file."
    assert "Error: The file at" in captured.out, "Should print specific error message"
    assert str(non_existent) in captured.out, "Error message should include the attempted path"

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


def test_poem_files_are_not_empty(tmp_path):
    """Test that when read_poem_folder_and_return_names is called empty files are not included."""

    poem_file_names = read_poem_folder_and_return_names(tmp_path)

    for poem_file_name in poem_file_names:
        poem_file_path = Path(tmp_path) / poem_file_name
        poem_content = read_poem_file_and_return_content(str(poem_file_path))
        assert poem_content.strip() != "", f"Poem file {poem_file_name} is empty."



def test_read_multiple_poem_files_and_write_analyses(tmp_path: Path):
    """Verify that multiple non-empty poem files get analysis files created."""
    #   Arrange 

    poem_folder = tmp_path / "poems"
    poem_folder.mkdir()

    test_poems = {
        "poem1.txt": "First line\nSecond line\nThird line",
        "poem2.txt": "Single stanza poem\nWith two lines",
        "poem3.txt": "Another poem\nMultiple lines\nIn one stanza",
        "empty.txt": "",                     # should be ignored
        "only-spaces.txt": "   \n\t\n  ",    # should be ignored
    }

    for name, content in test_poems.items():
        (poem_folder / name).write_text(content)


    # Call the real function, but point it to controlled folder
    read_multiple_poem_files_and_write_analyses(folder_path=str(poem_folder))

    #   Assert

    analysis_files = list(poem_folder.glob("*_analysis.txt"))
    assert len(analysis_files) == 3, f"Expected 3 analyses, got {len(analysis_files)}"

    for analysis_path in analysis_files:
        content = analysis_path.read_text(encoding="utf-8").strip()
        assert content, f"Analysis file is empty: {analysis_path.name}"
        assert "Stanza" in content, f"Analysis looks invalid: {analysis_path.name}"

    # Optional extra checks
    created_poem_names = {p.stem.removesuffix("_analysis") for p in analysis_files}
    expected = {"poem1", "poem2", "poem3"}

    assert created_poem_names == expected, \
    f"Wrong poems were analyzed: got {created_poem_names}"

    # Confirm empty files were skipped
    assert not (poem_folder / "empty_analysis.txt").exists()
    assert not (poem_folder / "only-spaces_analysis.txt").exists()

def test_read_multiple_poem_files_with_empty_folder(tmp_path, monkeypatch):
    """Test that function handles empty folder gracefully."""
    
    monkeypatch.chdir(tmp_path)
    empty_folder = tmp_path / "user poems"
    empty_folder.mkdir()
    
    read_multiple_poem_files_and_write_analyses()
    
    # No analysis files should be created
    analysis_files = list(empty_folder.glob("*_analysis.txt"))
    assert len(analysis_files) == 0, "No analysis files should be created for empty folder"