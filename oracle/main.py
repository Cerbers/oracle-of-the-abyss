"""
Main module for the Oracle Poetry Analyzer.
"""

from oracle.analyzer import analyze_poem
from pathlib import Path
from oracle.poem_model import Poem
from oracle.intern.lookout import watch_running_time_of_function

# TODO improve read_poem_file_and_return_content with error handling
# TODO improve write_poem_analysis to format analysis nicely



def read_poem_folder_and_return_names(folder_path: str) -> list[str]:
    """
    Reads only .txt and .md files' names from the specified folder and returns a 
    list that contains names of those files.
    
    Args:
        folder_path: The path to the folder containing poem files.
    
    Returns:
        A list of poem file names.
    """

    poem_texts = []
    folder = Path(folder_path)

    # Support both .txt and .md files
    for file_path in list(folder.glob("*.txt")) + list(folder.glob("*.md")):
        if not file_path.name.endswith("_analysis.txt"):
            with open(file_path, 'r', encoding='utf-8') as file:
                if file.read().strip() != "":
                    poem_texts.append(file_path.name)
    return poem_texts



def read_poem_file_and_return_content(file_path: str) -> str:
    """
    Reads a poem from a text file and returns its content.
    
    Args:
        file_path: The path to the poem file.
    
    Returns:
        The content of the poem file, or empty string if file not found.
    
    Note:
        Uses UTF-8 encoding and handles FileNotFoundError gracefully.
    """


    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            poem_text = file.read()
        return poem_text
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return ""
    
def write_poem_analysis(file_path: str) -> None:
    """
    Analyzes a poem and writes the results to a text file.
    
    Args:
        file_path: The path to the poem file to analyze.
    
    Note:
        Creates an output file with '_analysis.txt' suffix containing
        stanza breakdowns, line counts, and syllable counts.
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


@watch_running_time_of_function
def read_multiple_poem_files_and_write_analyses(folder_path: str = "user poems") -> None:
    """
    Processes all poem files in a folder and generates analysis files.
    
    Args:
        folder_path: The path to the folder containing poem files.
    
    Note:
        Skips files ending with '_analysis.txt' to avoid reprocessing.
        Prints progress and error messages to console.
    """

    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print(f"Error: The directory '{folder_path}' does not exist or is not a directory.")
        return

    poem_file_names = read_poem_folder_and_return_names(folder_path)

    if not poem_file_names:
        print(f"No valid poems found in '{folder_path}'.")
        return

    for poem_file_name in poem_file_names:
        poem_file_path = folder / poem_file_name
        write_poem_analysis(str(poem_file_path))


if __name__ == "__main__":
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="Oracle of the Abyss - Poem Analyzer")
    parser.add_argument("--perf", action="store_true", help="Enable performance monitoring")
    parser.add_argument("--folder", type=str, default="user poems", help="Folder containing poems (relative or absolute path)")
    args = parser.parse_args()

    if args.perf:
        os.environ["ORACLE_LOOKOUT"] = "1"

    read_multiple_poem_files_and_write_analyses(folder_path=args.folder)