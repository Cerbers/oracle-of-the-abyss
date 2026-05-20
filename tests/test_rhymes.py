



from oracle.analysis.rhymes import detect_rhymes
from oracle.domain_objects import Stanza, Line
import pytest

# ---------------------------------------------------------------------------
# detect_rhymes tests
# ---------------------------------------------------------------------------




@pytest.mark.parametrize("lines_text,expected", [
    # AABB – Rhyming Couplets: awake/break share EY1 K, dark/mark share AA1 R K
    (
        [
            "I lie awake",
            "before the break",
            "alone in the dark",
            "without a mark",
        ],
        ["AABB", "Rhyming Couplets"],
    ),
    # ABAB – Alternating Rhyme: day/way share EY1, night/light share AY1 T
    (
        [
            "I walked all day",
            "beneath the night",
            "and found my way",
            "by fading light",
        ],
        ["ABAB", "Alternating Rhyme"],
    ),
    # ABBA – Enclosed Rhyme: gate/fate share EY1 T, night/light share AY1 T
    (
        [
            "I stood before the gate",
            "and watched the falling night",
            "until the morning light",
            "decided by my fate",
        ],
        ["ABBA", "Enclosed Rhyme"],
    ),
    # Monorhyme: love/above/dove/shove all share AH1 V
    (
        [
            "I think of love",
            "the stars above",
            "the morning dove",
            "a gentle shove",
        ],
        ["AAAA", "Monorhyme"],
    ),
    # No named scheme – ABCB (sky/die rhyme, earth and home don't)
    (
        [
            "I walk the earth",
            "beneath the sky",
            "in search of home",
            "before I die",
        ],
        ["ABCB", "No recognized rhyme pattern"],
    ),
    # Fewer than 2 lines → empty
    (
        ["Only one line here"],
        [],
    ),
])
def test_rhyme_detection_scenarios(lines_text, expected):
    """Test rhyme scheme detection across named and unnamed patterns."""
    stanza = Stanza(lines=[Line(text=t) for t in lines_text])
    result = detect_rhymes(stanza)
    assert result == expected