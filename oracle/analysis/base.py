from oracle.poem_model import Poem
from oracle.domain_objects import Stanza




def anaphora(poem_stanza: Stanza) -> list[str]:
    if len(poem_stanza.lines) < 2:
        return []
    
    best_matches: list[str] = []
    
    # Try patterns from 2 words up to (max words per line - 1)
    max_words_per_line = max(len(line.text.split()) for line in poem_stanza.lines)
    max_pattern_length = max_words_per_line - 1  # Don't use full lines
    
    for pattern_length in range(2, max_pattern_length + 1):
        current_matches = []
        
        # Get all patterns of this length
        patterns = []
        for line in poem_stanza.lines:
            words = line.text.split()
            if len(words) >= pattern_length:
                pattern = ' '.join(words[:pattern_length]).lower().strip('.,!?":;')
                patterns.append(pattern)
        
        # Count pattern frequencies
        pattern_counts: dict[str, int] = {}
        for pattern in patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        # Find patterns with max matches for this length
        max_count = max(pattern_counts.values()) if pattern_counts else 0
        if max_count > 1:  # At least 2 matches
            for pattern, count in pattern_counts.items():
                if count == max_count:
                    current_matches.extend([pattern] * count)
        
        # Update best if this pattern length has same or more matches
        if len(current_matches) >= len(best_matches) and len(current_matches) > 0:
            best_matches = current_matches
    
    return best_matches