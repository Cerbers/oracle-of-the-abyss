from oracle.poem_model import Poem
from oracle.syllable_counter import count_syllables_in_line

# TODO find a way to not count title if poem has one in the text file
# TODO have line count and syllable count show at end of each stanza



def analyze_poem(poem: Poem) -> dict[str, str | int | list[int]]:
    lines_with_text = []
    for line in poem.text.split('\n'):
        if check_for_title_line(line, poem):
            continue
        if line.strip():
            lines_with_text.append(line)

    syllables_per_line = [count_syllables_in_line(line) for line in lines_with_text]

    return {
        "poem": poem.text,
        "Lines": len(lines_with_text),
        "Syllables_per_line": syllables_per_line
    }

def check_for_title_line(line: str, poem: Poem) -> bool:
    """Check if the poem has a title line enclosed in quotes, all caps, 
    or if the first line is significantly shorter than the rest and coincides with file name."""

    stripped = line.strip()

    if stripped.startswith('"') and stripped.endswith('"'):
        return True

    if stripped.isupper():
        return True

    if stripped == poem.filename:
        return True

    return False