from oracle.analysis.base import anaphora
from oracle.domain_objects import Stanza, Line
import pytest

@pytest.mark.parametrize("lines_text,expected_patterns", [
    # Test 1: Original case - 3-word anaphora in first 2 lines
    ([
        "fear not the night",
        "fear not the light", 
        "fear the lie"
    ], ["fear not the", "fear not the"]),
    
    # Test 2: 2-word anaphora in middle lines (lines 3-4)
    ([
        "I walk alone",
        "I dream tonight", 
        "in the shadows",
        "in the darkness",
        "I find my way"
    ], ["in the", "in the"]),
    
    # Test 3: Multiple anaphora patterns - prefers shorter with more matches
    ([
        "when the morning comes",
        "when the morning breaks",
        "when the night falls",
        "when the stars appear"
    ], ["when the", "when the", "when the", "when the"]),
    
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
    
    # Test 6: Mixed case and punctuation (actual behavior)
    ([
        "Oh! Captain, my Captain",
        "oh! captain, my captain",
        "Oh! Captain, our leader"
    ], ["oh! captain", "oh! captain", "oh! captain"]),
    
    # Test 7: Longer anaphora with 5 lines, repetition in lines 2-3
    ([
        "I remember the summer days",
        "I remember the summer nights", 
        "I remember the summer dreams",
        "Winter comes and goes away",
        "Spring brings new life again"
    ], ["i remember the summer", "i remember the summer", "i remember the summer"]),
    
    # Test 8: Edge case - exactly 2 lines with anaphora
    ([
        "Love is patient and kind",
        "Love is patient and true"
    ], ["love is patient and", "love is patient and"]),
    
    # Test 9: Different pattern lengths - prefers shorter with more matches
    ([
        "give me liberty or death",
        "give me liberty or freedom",
        "give me peace and quiet"
    ], ["give me", "give me", "give me"]),
    
    # Test 10: Lines with different lengths
    ([
        "A",
        "A B",
        "A B C", 
        "A B D"
    ], ["a b", "a b", "a b"])
])
def test_anaphora_scenarios(lines_text, expected_patterns):
    """Test various anaphora scenarios with different patterns and line counts."""
    test_lines = [Line(text=text) for text in lines_text]
    test_stanza = Stanza(lines=test_lines)
    
    result = anaphora(test_stanza)
    assert result == expected_patterns