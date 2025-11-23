from oracle.analyzer import analyze_poem
# TODO open and read text file, analyze it then write a new file with results
# TODO improve read_poem_file with error handling


def read_poem_file(file_path: str) -> str:
    """Reads a poem from a text file and returns its content."""

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            poem_text = file.read()
        return poem_text
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return ""