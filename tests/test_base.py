from oracle.analysis.base import anaphora
from oracle.domain_objects import Stanza, Line
import pytest


@pytest.mark.parametrize("lines_text,expected_patterns", [
    # Test 1: 3-word anaphora in first 2 lines
    ([
        "fear not the night",
        "fear not the light",
        "fear the lie"
    ], ["2x fear not the"]),

    # Test 2: 2-word anaphora in consecutive middle lines (lines 3-4)
    ([
        "I walk alone",
        "I dream tonight",
        "in the shadows",
        "in the darkness",
        "I find my way"
    ], ["2x in the"]),

    # Test 3: All 4 lines share 2-word prefix; longer prefix only covers 2 → 2-word wins
    ([
        "when the morning comes",
        "when the morning breaks",
        "when the night falls",
        "when the stars appear"
    ], ["4x when the"]),

    # Test 4: No anaphora patterns
    ([
        "I walk alone tonight",
        "The stars are shining bright",
        "Moonlight on the water",
        "Dreams of distant shores"
    ], []),

    # Test 5: Single word repeated (should not detect - minimum 2 words)
    ([
        "the wind blows",
        "the trees sway",
        "the birds sing",
        "the river flows"
    ], []),

    # Test 6: Mixed case and punctuation
    ([
        "Oh! Captain, my Captain",
        "oh! captain, my captain",
        "Oh! Captain, our leader"
    ], ["3x oh! captain"]),

    # Test 7: 3-line consecutive run; longer prefix keeps winning on equal run length
    ([
        "I remember the summer days",
        "I remember the summer nights",
        "I remember the summer dreams",
        "Winter comes and goes away",
        "Spring brings new life again"
    ], ["3x i remember the summer"]),

    # Test 8: Exactly 2 consecutive lines with anaphora
    ([
        "Love is patient and kind",
        "Love is patient and true"
    ], ["2x love is patient and"]),

    # Test 9: "give me" spans all 3 lines (run=3) vs "give me liberty" spans only 2 → "give me" wins
    ([
        "give me liberty or death",
        "give me liberty or freedom",
        "give me peace and quiet"
    ], ["3x give me"]),

    # Test 10: Lines with different lengths (line 1 too short for 2-word prefix)
    ([
        "A",
        "A B",
        "A B C",
        "A B D"
    ], ["3x a b"]),

    # Test 11: Non-consecutive "for the" must NOT be detected
    # "For the" appears in lines 3 and 5 but line 4 sits between them
    ([
        "Atom-less eons passed",
        "Life's been punished",
        "For the hope it held",
        "cosmic model dissolved",
        "For the chains of cruel fate it grants",
        'so "mercifully"',
    ], []),

    # Test 12: Consecutive detection still works correctly
    ([
        "For the morning light",
        "For the evening dark",
        "Something else entirely",
    ], ["2x for the"]),
])
def test_anaphora_scenarios(lines_text, expected_patterns):
    """Test various anaphora scenarios with different patterns and line counts."""
    test_lines = [Line(text=text) for text in lines_text]
    test_stanza = Stanza(lines=test_lines)

    result = anaphora(test_stanza)
    assert result == expected_patterns


