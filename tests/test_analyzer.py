from pathlib import Path
from oracle.poem_model import Poem
from oracle.analyzer import analyze_poem


# TODO expand test cases for edge cases


def test_analyze_poem_has_stanzas_in_list():
    """Test the poem analyzer function returns stanza texts, line counts, and syllable counts."""

    poem = """"Voidborn"
    Born out of the void
    Amidst the stars of flesh
    An illusion both full and empty
    O'er the abyss' watchful maw
    
    Gazes into the weary eyes of a lost stalker
    Who lies in blood-flow of the night
    """
    
    poem_obj = Poem(text=poem, filepath=Path("test_poem.txt"))
    analysis = analyze_poem(poem_obj)

    expected = {
        'stanza_texts': [
            "Born out of the void\nAmidst the stars of flesh\nAn illusion both full and empty\nO'er the abyss' watchful maw",
            "Gazes into the weary eyes of a lost stalker\nWho lies in blood-flow of the night"
        ],
        'line_counts': [4, 2],
        'syllables_per_line': [[5, 6, 9, 7], [13, 8]]
    }
    
    assert analysis == expected, f"Poem analysis did not match expected output. Instead got: {analysis}"