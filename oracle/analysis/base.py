from oracle.domain_objects import Stanza
# TODO: Revise anaphora function

def anaphora(poem_stanza: Stanza) -> list[str]:
    """
    Analyzes a stanza for anaphora (repetition of word patterns at line beginnings).

    Only consecutive lines are considered: a pattern must appear on adjacent lines
    without interruption to qualify as anaphora.

    Args:
        poem_stanza: The stanza to analyze.

    Returns:
        A single-element list ``["Nx phrase"]`` where N is the run length and
        ``phrase`` is the repeated opening, or ``[]`` if no anaphora is found.
    """
    if len(poem_stanza.lines) < 2:
        return []

    best_pattern: str | None = None
    best_count: int = 0

    max_words_per_line = max(len(line.text.split()) for line in poem_stanza.lines)
    max_pattern_length = max_words_per_line - 1  # never use a full line as the pattern

    for pattern_length in range(2, max_pattern_length + 1):
        # Build per-line patterns; None when a line is too short to have this prefix
        line_patterns: list[str | None] = []
        for line in poem_stanza.lines:
            words = line.text.split()
            if len(words) >= pattern_length:
                prefix = ' '.join(words[:pattern_length]).lower().strip('.,!?":;')
                line_patterns.append(prefix)
            else:
                line_patterns.append(None)

        # Walk through and find the longest consecutive run of the same prefix
        i = 0
        while i < len(line_patterns):
            if line_patterns[i] is None:
                i += 1
                continue
            current = line_patterns[i]
            j = i + 1
            while j < len(line_patterns) and line_patterns[j] == current:
                j += 1
            run_length = j - i
            # >= so that a longer prefix wins over a shorter one with the same run
            if run_length >= 2 and run_length >= best_count:
                best_count = run_length
                best_pattern = current
            i = j

    if best_pattern is None:
        return []
    return [f"{best_count}x {best_pattern}"]


