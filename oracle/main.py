"""Main module for poem file operations and analysis workflow.

This module provides functionality to read poem files from disk,
analyze their content, and write analysis results back to files.
It serves as the entry point for batch poem processing.
"""

from oracle.analyzer import analyze_poem
from pathlib import Path
from oracle.poem_model import Poem

# TODO improve read_poem_file_and_return_content with error handling
# TODO improve write_poem_analysis to format analysis nicely
# TODO: Add user input via CLI


def read_poem_folder_and_return_names(folder_path: str) -> list[str]:
    """Read and return the names of non-empty poem files from a folder.

    Scans the specified folder for .txt files that are not analysis files
    (files ending with '_analysis.txt') and are not empty.

    Args:
        folder_path: Path to the folder containing poem files.

    Returns:
        A list of filenames (including .txt extension) for valid poem files.
        Empty files and analysis files are excluded from the result.

    Example:
        >>> names = read_poem_folder_and_return_names("user poems")
        >>> print(names)
        ['The Serpent.txt', 'Voidborn.txt']
    """
    poem_texts = []
    folder = Path(folder_path)

    for file_path in folder.glob("*.txt"):
        if not file_path.name.endswith("_analysis.txt"):
            with open(file_path, 'r', encoding='utf-8') as file:
                if file.read().strip() != "":
                    poem_texts.append(file_path.name)
    return poem_texts


def read_poem_file_and_return_content(file_path: str) -> str:
    """Read a poem file and return its text content.

    Opens and reads the entire content of a poem file. If the file
    cannot be found, an error message is printed and an empty string
    is returned.

    Args:
        file_path: Path to the poem text file.

    Returns:
        The content of the poem file as a string, or an empty string
        if the file was not found.

    Example:
        >>> content = read_poem_file_and_return_content("user poems/The Serpent.txt")
        >>> print(content[:20])
        '"The Serpent"\\nCoiled'
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            poem_text = file.read()
        return poem_text

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return ""


def write_poem_analysis(file_path: str) -> None:
    """Analyze a poem file and write the analysis to a new file.

    Reads a poem from the specified file, performs structural analysis
    (stanzas, line counts, syllable counts), and writes the results
    to a new file with '_analysis.txt' suffix.

    Args:
        file_path: Path to the poem text file to analyze.

    Returns:
        None. Creates an analysis file in the same directory as the input.

    Example:
        >>> write_poem_analysis("user poems/Voidborn.txt")
        # Creates "user poems/Voidborn_analysis.txt" with analysis results
    """
    input_path = Path(file_path)

    poem_text = read_poem_file_and_return_content(file_path)
    poem_obj = Poem(text=poem_text, filepath=input_path)

    analysis_result = analyze_poem(poem_obj)

    output_path = input_path.with_name(input_path.stem + "_analysis.txt")
    with open(output_path, 'w', encoding='utf-8') as file:
        # Iterate through each stanza's data together
        for i, (text, line_count, syllables) in enumerate(
            zip(
                analysis_result['stanza_texts'],
                analysis_result['line_counts'],
                analysis_result['syllables_per_line']
            ), start=1
        ):
            file.write(f"Stanza {i}:\n")
            file.write(f"{text}\n")
            file.write(f"Lines: {line_count}\n")
            file.write(f"Syllables per line: {syllables}\n\n")


def read_multiple_poem_files_and_write_analyses() -> None:
    """Process all poem files in the 'user poems' folder.

    Reads all valid poem files from the 'user poems' directory and
    creates corresponding analysis files for each one.

    Returns:
        None. Creates analysis files for each poem in the folder.

    Example:
        >>> read_multiple_poem_files_and_write_analyses()
        # Processes all .txt files in 'user poems' and creates analysis files
    """
    poem_file_names = read_poem_folder_and_return_names("user poems")

    for poem_file_name in poem_file_names:
        poem_file_path = Path("user poems") / poem_file_name
        write_poem_analysis(str(poem_file_path))


if __name__ == "__main__":
    read_multiple_poem_files_and_write_analyses()