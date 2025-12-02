from oracle.poem_model import Poem, Line, Stanza

def analyze_poem(poem: Poem) -> dict[str, list]:
    """Analyze poem using domain objects for flexible syllable pattern detection."""
    
    stanza_texts = []
    line_counts = []
    syllables_per_line = []
    
    # Convert raw string stanzas into Stanza objects
    for stanza_lines in poem.stanzas:  # list[list[str]]
        # Create Line objects from strings
        line_objects = [Line(text=line) for line in stanza_lines]
        
        # Create Stanza object
        stanza_obj = Stanza(lines=line_objects)
        
        # Now work with the object model
        stanza_texts.append(stanza_obj.stanza_text_string)
        line_counts.append(len(stanza_obj.lines))
        
        # Get syllable counts from Line objects
        stanza_syllables = [line.get_total_syllables() for line in stanza_obj.lines]
        syllables_per_line.append(stanza_syllables)
    
    return {
        'stanza_texts': stanza_texts,
        'line_counts': line_counts,
        'syllables_per_line': syllables_per_line
    }