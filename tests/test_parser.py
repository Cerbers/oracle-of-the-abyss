from pathlib import Path

from oracle.poem_model import Poem
from oracle.domain_objects import Stanza, Line
from oracle.parser import parse_into_stanzas



def test_parse_into_stanzas():
    """Test that poem text is correctly parsed into stanzas (lists of Line objects).
    Stanzas are separated by blank lines where blank line/s count in between is n >=1."""

    case_poem_texts = {
        "Case 1": """"Voidborn"
    Born out of the void
    Amidst the stars of flesh
    An illusion both full and empty
    O'er the abyss' watchful maw
    
    Gazes into the weary eyes of a lost stalker""",
        "Case 2": """"Voidborn"
    Born out of the void
    Amidst the stars of flesh
    An illusion both full and empty
    O'er the abyss' watchful maw
    

    Gazes into the weary eyes of a lost stalker""",
        "Case 3": """Voidborn
        
        Born out of the void
        Amidst the stars of flesh
        An illusion both full and empty
        O'er the abyss' watchful maw
        
        Gazes into the weary eyes of a lost stalker"""
    }
    # fake text to not throw error in Poem object
    CasePoemObject = Poem(text="filler", filepath=Path("Voidborn.txt"))

    for case_name, poem_text in case_poem_texts.items():
        stanzas = parse_into_stanzas(poem_text, CasePoemObject.filename)
        assert len(stanzas) == 2, f"{case_name} failed to parse into 2 stanzas."
        assert all(isinstance(stanza, Stanza) for stanza in stanzas), f"{case_name} stanzas are not Stanza objects."
        assert all(isinstance(line, Line) for stanza in stanzas for line in stanza.lines), f"{case_name} lines are not Line objects."
        assert stanzas[0].lines[0].text.strip().startswith("Born out of the void"), f"{case_name} first stanza first line incorrect."


