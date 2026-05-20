"""
Analyzer module for poem analysis.
"""

from oracle.poem_model import Poem
# from oracle.domain_objects import Stanza
from oracle.intern.lookout import watch_running_time_of_function
from oracle.analysis.base import anaphora
from oracle.analysis.rhymes import detect_rhymes


POETIC_ANALYZERS = {
    'anaphora': anaphora,
    'rhymes': detect_rhymes,
}


# TODO: break the analyze_poem to create pipeline for anlysis efficiently
@watch_running_time_of_function
def analyze_poem(poem: Poem) -> dict[str, list[str] | list[int] | list[list[int]] | list[dict[str, list[str]]]]:
    """
    Analyze poem using domain objects.
    """
    analysis_baseline = create_analysis_baseline(poem)
    
    # List comprehension to create poetic results for each stanza
    poetic_results = [
        {
            'anaphora': anaphora(stanza),
            'rhymes': detect_rhymes(stanza)
        }
        for stanza in poem.stanzas
    ]
    
    analysis_baseline['poetic_devices'] = poetic_results   # now a list of dicts (one per stanza)
    return analysis_baseline


# TODO: Add tests
def create_analysis_baseline(poem: Poem) -> dict:
    """
    Only the fast structural stuff. Poetic analyses are moved to the parallel runner.
    """
    stanza_texts = []
    line_counts = []
    syllables_per_line = []
    
    for stanza_obj in poem.stanzas:  
        stanza_texts.append(stanza_obj.stanza_text_string)
        line_counts.append(len(stanza_obj.lines))

        stanza_syllables = [line.get_total_syllables() for line in stanza_obj.lines]
        syllables_per_line.append(stanza_syllables)
    
    return {
        'stanza_texts': stanza_texts,
        'line_counts': line_counts,
        'syllables_per_line': syllables_per_line,
        # 'poetic_devices' is added afterwards in analyze_poem
    }