from oracle.poem_model import Poem
from oracle.intern.lookout import watch_running_time_of_function



# @watch_running_time_of_function
def analyze_poem(poem: Poem) -> dict[str, list[str] | list[int] | list[list[int]]]:
    """Analyze poem using domain objects for flexible syllable pattern detection."""
    
    stanza_texts = []
    line_counts = []
    syllables_per_line = []
    
    # Convert raw string stanzas into Stanza objects
    for stanza_obj in poem.stanzas:  
        stanza_texts.append(stanza_obj.stanza_text_string)
        line_counts.append(len(stanza_obj.lines))
        stanza_syllables = [line.get_total_syllables() for line in stanza_obj.lines]
        syllables_per_line.append(stanza_syllables)
    
    return {
        'stanza_texts': stanza_texts,
        'line_counts': line_counts,
        'syllables_per_line': syllables_per_line
    }