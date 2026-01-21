from pathlib import Path
from oracle.devices import analyze_anaphora, holder_for_poetic_device_analysis
from oracle.poem_model import Poem


class TestAnalyzeAnaphora:
    def test_detects_anaphora_chain(self):
        """Test that anaphora is detected when consecutive lines start with the same two words."""
        poem_text = """I am the void
I am the darkness
I am the abyss
Something else here"""

        result = analyze_anaphora(poem_text)

        assert len(result) == 1
        assert result[0] == [("I", "am"), ("I", "am"), ("I", "am")]

    def test_no_anaphora_when_lines_differ(self):
        """Test that no anaphora is detected when consecutive lines start differently."""
        poem_text = """The sun rises
A bird sings
The moon sets"""

        result = analyze_anaphora(poem_text)

        assert result == []

    def test_empty_poem_returns_empty_list(self):
        """Test that an empty poem returns an empty list."""
        poem_text = ""

        result = analyze_anaphora(poem_text)

        assert result == []

    def test_ignores_blank_lines(self):
        """Test that blank lines are ignored when detecting anaphora."""
        poem_text = """I am the void

I am the darkness

I am the abyss"""

        result = analyze_anaphora(poem_text)

        assert len(result) == 1
        assert result[0] == [("I", "am"), ("I", "am"), ("I", "am")]

    def test_respects_min_chain_length_for_final_chain(self):
        """Test that final chain shorter than min_chain_length is not returned."""
        poem_text = """Something else
I am one
I am two"""

        result = analyze_anaphora(poem_text, min_chain_length=3)

        assert result == []

    def test_custom_min_chain_length(self):
        """Test that custom min_chain_length is respected."""
        poem_text = """I am one
I am two
Something else"""

        result = analyze_anaphora(poem_text, min_chain_length=2)

        assert len(result) == 1
        assert result[0] == [("I", "am"), ("I", "am")]

    def test_multiple_anaphora_chains(self):
        """Test that multiple separate anaphora chains are detected."""
        poem_text = """We are the beginning
We are the middle
We are the end
A break occurs
They were the past
They were the present
They were the future"""

        result = analyze_anaphora(poem_text)

        assert len(result) == 2
        assert result[0] == [("We", "are"), ("We", "are"), ("We", "are")]
        assert result[1] == [("They", "were"), ("They", "were"), ("They", "were")]

    def test_single_word_lines_do_not_break_chain(self):
        """Test that lines with only one word are skipped and don't break the chain."""
        poem_text = """I am here
Word
I am there
I am everywhere"""

        result = analyze_anaphora(poem_text)

        assert len(result) == 1
        assert result[0] == [("I", "am"), ("I", "am"), ("I", "am")]

    def test_whitespace_is_stripped(self):
        """Test that leading/trailing whitespace is stripped from lines."""
        poem_text = """   I am the void
  I am the darkness
    I am the abyss"""

        result = analyze_anaphora(poem_text)

        assert len(result) == 1
        assert result[0] == [("I", "am"), ("I", "am"), ("I", "am")]


class TestHolderForPoeticDeviceAnalysis:
    def test_returns_anaphora_results(self):
        """Test that the holder function returns anaphora analysis results."""
        poem_text = """I am the void
I am the darkness
I am the abyss"""
        poem = Poem(text=poem_text, filepath=Path("test_poem.txt"))

        result = holder_for_poetic_device_analysis(poem)

        assert len(result) == 1
        assert result[0] == [("I", "am"), ("I", "am"), ("I", "am")]