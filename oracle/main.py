from oracle.analyzer import analyze_poem
from pathlib import Path
from oracle.devices import holder_for_poetic_device_analysis
from oracle.poem_model import Poem
from oracle.intern.lookout import watch_running_time_of_function

# TODO improve read_poem_file_and_return_content with error handling
# TODO improve write_poem_analysis to format analysis nicely
# TODO: Add user input via CLI



def read_poem_folder_and_return_names(folder_path: str) -> list[str]:
    """    Reads only .txt files' names from the specified folder and returns a 
    list that contains names of those files."""

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

    poem_text = read_poem_file_and_return_content(file_path)
    poem_obj = Poem(text=poem_text, filepath=input_path)

    # WiP poetic device analysis
    poetic_devices_found = holder_for_poetic_device_analysis(poem_obj)

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
        for device in poetic_devices_found:
            file.write(f"Anaphora found: {device}\n")


# @watch_running_time_of_function
def read_multiple_poem_files_and_write_analyses(folder_path: str = "user poems") -> None:
    """Reads multiple poem files from 'user poems' folder and writes their analyses."""

    poem_file_names = read_poem_folder_and_return_names(folder_path)

    for poem_file_name in poem_file_names:
        poem_file_path = Path(folder_path) / poem_file_name
        write_poem_analysis(str(poem_file_path))


if __name__ == "__main__":
    read_multiple_poem_files_and_write_analyses()