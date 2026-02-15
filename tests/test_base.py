from oracle.analysis.base import anaphora
from oracle.domain_objects import Stanza, Line

def test_anaphora_positive():
    # test with simple poem for anaphora detection and that it returns a list of repetitions
    test_lines = [
        Line(text="fear not the night"),
        Line(text="fear not the light"),
        Line(text="fear the lie")
    ]
    test_stanza = Stanza(lines=test_lines)
    
    result = anaphora(test_stanza)
    assert result == ["fear not the", "fear not the"]