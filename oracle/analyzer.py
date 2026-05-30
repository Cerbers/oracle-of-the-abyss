"""
Analyzer module for poem analysis.
"""

from typing import TypedDict

from oracle.poem_model import Poem
from oracle.intern.lookout import watch_running_time_of_function
from oracle.analysis.base import anaphora
from oracle.analysis.rhymes import detect_rhymes


class AnalysisResult(TypedDict):
    stanza_texts: list[str]
    line_counts: list[int]
    syllables_per_line: list[list[int]]
    poetic_devices: list[dict[str, list[str]]]

POETIC_ANALYZERS = {
    'anaphora': anaphora,
    'rhymes': detect_rhymes,
}



@watch_running_time_of_function
def analyze_poem(poem: Poem) -> AnalysisResult:
    """
    Analysis orchestration function. Calls create_analysis_baseline to get baseline data
    and then analyzes each stanza for poetic devices.

    Args:
        poem: The poem to analyze

    Returns:
        AnalysisResult: Dictionary containing baseline data and poetic device analysis

    Note:
        This function is meant for organizing the analysis process.
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
def create_analysis_baseline(poem: Poem) -> AnalysisResult:
    """
    Creates baseline analysis data for a poem. Baseline data is a dictionary containing:
    - stanza_texts: list of stanza text strings
    - line_counts: list of line counts per stanza
    - syllables_per_line: list of syllable counts per line per stanza
    - poetic_devices: empty list to be filled with poetic device analysis
    """
    stanza_texts: list[str] = []
    line_counts: list[int] = []
    syllables_per_line: list[list[int]] = []
    
    for stanza_obj in poem.stanzas:  
        stanza_texts.append(stanza_obj.stanza_text_string)
        line_counts.append(len(stanza_obj.lines))

        stanza_syllables = [line.get_total_syllables() for line in stanza_obj.lines]
        syllables_per_line.append(stanza_syllables)
    
    return {
        'stanza_texts': stanza_texts,
        'line_counts': line_counts,
        'syllables_per_line': syllables_per_line,
        'poetic_devices': [],
    }


