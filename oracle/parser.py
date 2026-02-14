"""
Parser module for turning poem text into domain objects.
"""

from oracle.domain_objects import Line, Stanza
from oracle.utils import check_for_title_line

# TODO improve parse_into_stanzas to handle title cases when first line of other stanzas matches filename

def parse_into_stanzas(poem_text: str, poem_name: str) -> list[Stanza]:
    """
    Parse poem text into stanzas, separated by blank line/s.
     
    Args:
        poem_text (str): The raw poem text to parse.
        poem_name (str): The name of the poem, used to identify title lines.

    Returns:
        list[Stanza]: A list of Stanza objects, each containing Line objects.

    Note:
        The function strips leading/trailing whitespace from lines,
        and handles multiple consecutive blank lines as a single stanza separator.
        The function returns a list of stanzas, where each stanza is a list of its lines.
    """
    
    # TODO add accounting for multiple poems in single file

    cleaned_text = '\n'.join(line.strip() for line in poem_text.splitlines())
    stanzas=cleaned_text.split('\n\n')

    result = []
    for stanza in stanzas:
        lines = [line.strip('#*') for line in stanza.split('\n') if line.strip()]
        if check_for_title_line(lines[0], poem_name):
            lines = lines[1:]
        if lines:
            # Create Line objects here
            line_objects = [Line(text=line) for line in lines]
            stanza_obj = Stanza(lines=line_objects)
            result.append(stanza_obj)
    return result