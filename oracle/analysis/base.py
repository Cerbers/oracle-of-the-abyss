from oracle.poem_model import Poem
from oracle.domain_objects import Stanza


stanzas = []

def poetic_devices(poem: Poem) -> list[Stanza]:
    for stanza in poem.stanzas:
        stanzas.append(stanza)
    return stanzas


def anaphora(poem_stanza: Stanza) -> None: 
    # take first half of lines (n/2)
    half_lines = poem_stanza.lines[:len(poem_stanza.lines) // 2]

    if len(half_lines) <2:
        return []

    # start with 2-word patterns
    pattern_length = 2

    # get first pattern from line 1
    words = half_lines[0].text.split()
    if len(words) < pattern_length:
        return []
        
    current_pattern = ' '.join(words[:pattern_length]).lower().strip('.,!?":;')
    matches = [current_pattern]
    
    # Compare with subsequent lines
    for line in half_lines[1:]:
        words = line.text.split()
        if len(words) >= pattern_length:
            line_pattern = ' '.join(words[:pattern_length]).lower().strip('.,!?":;')
            if line_pattern == current_pattern:
                matches.append(line_pattern)
            else:
                # Use this line's pattern as new comparison
                current_pattern = line_pattern
                matches = [current_pattern]
    
    # Return patterns that appeared more than once
    return matches if len(matches) > 1 else []