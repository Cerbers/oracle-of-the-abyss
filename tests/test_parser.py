import pytest
from pathlib import Path

from oracle.poem_model import Poem
from oracle.domain_objects import Stanza, Line
from oracle.parser import parse_into_stanzas


# Test data: poems with title + two stanzas separated by varying blank lines
POEM_WITH_QUOTED_TITLE_SINGLE_BLANK = """"Voidborn"
Born out of the void
Amidst the stars of flesh
An illusion both full and empty
O'er the abyss' watchful maw

Gazes into the weary eyes of a lost stalker"""

POEM_WITH_QUOTED_TITLE_DOUBLE_BLANK = """"Voidborn"
Born out of the void
Amidst the stars of flesh
An illusion both full and empty
O'er the abyss' watchful maw


Gazes into the weary eyes of a lost stalker"""

POEM_WITH_UNQUOTED_TITLE = """Voidborn

Born out of the void
Amidst the stars of flesh
An illusion both full and empty
O'er the abyss' watchful maw

Gazes into the weary eyes of a lost stalker"""

POEM_WITH_MARKDOWN = """
###Born out of the void
Amidst the stars of flesh
###An illusion both full and empty
*O'er the abyss' watchful maw*

Gazes into the weary eyes of a lost stalker
"""


@pytest.fixture
def poem_filename():
    """Provide a filename for parse_into_stanzas."""
    return Poem(text="filler", filepath=Path("Voidborn.txt")).filename


class TestParseIntoStanzas:
    """Tests for parse_into_stanzas function."""

    @pytest.mark.parametrize("poem_text,description", [
        (POEM_WITH_QUOTED_TITLE_SINGLE_BLANK, "quoted title, single blank line separator"),
        (POEM_WITH_QUOTED_TITLE_DOUBLE_BLANK, "quoted title, double blank line separator"),
        (POEM_WITH_UNQUOTED_TITLE, "unquoted title, single blank line separator"),
    ])
    def test_parses_correct_number_of_stanzas(self, poem_text, description, poem_filename):
        """Stanzas are separated by one or more blank lines."""
        stanzas = parse_into_stanzas(poem_text, poem_filename)
        assert len(stanzas) == 2, f"Failed for: {description}"

    @pytest.mark.parametrize("poem_text,description", [
        (POEM_WITH_QUOTED_TITLE_SINGLE_BLANK, "quoted title"),
        (POEM_WITH_UNQUOTED_TITLE, "unquoted title"),
    ])
    def test_returns_stanza_objects(self, poem_text, description, poem_filename):
        """Each parsed stanza should be a Stanza instance."""
        stanzas = parse_into_stanzas(poem_text, poem_filename)
        assert all(isinstance(stanza, Stanza) for stanza in stanzas), f"Failed for: {description}"

    @pytest.mark.parametrize("poem_text,description", [
        (POEM_WITH_QUOTED_TITLE_SINGLE_BLANK, "quoted title"),
        (POEM_WITH_UNQUOTED_TITLE, "unquoted title"),
    ])
    def test_stanzas_contain_line_objects(self, poem_text, description, poem_filename):
        """Each line within a stanza should be a Line instance."""
        stanzas = parse_into_stanzas(poem_text, poem_filename)
        for stanza in stanzas:
            assert all(isinstance(line, Line) for line in stanza.lines), f"Failed for: {description}"

    @pytest.mark.parametrize("poem_text,description", [
        (POEM_WITH_QUOTED_TITLE_SINGLE_BLANK, "quoted title"),
        (POEM_WITH_QUOTED_TITLE_DOUBLE_BLANK, "quoted title with double blank"),
        (POEM_WITH_UNQUOTED_TITLE, "unquoted title"),
    ])
    def test_title_is_stripped_from_content(self, poem_text, description, poem_filename):
        """First line of first stanza should be poem content, not title."""
        stanzas = parse_into_stanzas(poem_text, poem_filename)
        first_line = stanzas[0].lines[0].text.strip()
        assert first_line.startswith("Born out of the void"), f"Failed for: {description}"

    @pytest.mark.parametrize("poem_text,description", [
        (POEM_WITH_MARKDOWN, "markdown title"),
    ])
    def test_markdown_is_stripped_from_content(self, poem_text, description, poem_filename):
        """First line of first stanza should be poem content, not title."""
        stanzas = parse_into_stanzas(poem_text, poem_filename)
        first_line = stanzas[0].lines[0].text.strip()
        assert first_line.startswith("Born out of the void"), f"Failed for: {description}"