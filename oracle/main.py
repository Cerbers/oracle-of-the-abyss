from oracle.analyzer import analyze_poem
from pathlib import Path

# TODO improve read_poem_file_and_return_content with error handling
# TODO improve write_poem_analysis to format analysis nicely
# TODO: Add user input via CLI


def read_poem_folder_and_return_names(folder_path: str) -> list[str]:
    """ Reads only .txt files' names from the specified folder and returns a list that contains names of those files."""

    
    poem_texts = []
    folder = Path(folder_path)

    for file_path in folder.glob("*.txt"):
        if not file_path.name.endswith("_analysis.txt"):
            with open(file_path, 'r', encoding='utf-8') as file:
                if file.read().strip() != "":
                    poem_texts.append(file_path.name)
    return poem_texts



def read_poem_file_and_return_content(file_path: str) -> str:
    """Reads a poem from a text file and returns its content."""


    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            poem_text = file.read()
        return poem_text
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return ""
    
def write_poem_analysis(file_path: str) -> None:

    input_path = Path(file_path)

    poem_to_be_analysed = read_poem_file_and_return_content(file_path)
    analysis_result = analyze_poem(poem_to_be_analysed)
    
    output_path = input_path.with_name(input_path.stem + "_analysis.txt")
    with open(output_path, 'w', encoding='utf-8') as file:
        for key, value in analysis_result.items():
            file.write(f"{key}: {value}\n")


def read_multiple_poem_files_and_write_analyses() -> None:
    """Reads multiple poem files from 'user poems' folder and writes their analyses."""

    poem_file_names = read_poem_folder_and_return_names("user poems")

    for poem_file_name in poem_file_names:
        poem_file_path = Path("user poems") / poem_file_name
        write_poem_analysis(str(poem_file_path))

if __name__ == "__main__":
    read_multiple_poem_files_and_write_analyses()