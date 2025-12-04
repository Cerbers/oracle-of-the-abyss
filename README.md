# Oracle

A Python poetry analysis tool that counts syllables and identifies metrical patterns in poems.

## Overview

Oracle analyzes poems by breaking them into structural components (stanzas, lines, words) and counting syllables using the CMU Pronouncing Dictionary. The tool handles common poetic devices like contractions and elisions, making it suitable for analyzing both classical and contemporary poetry.

Built with modular architecture that separates parsing, analysis, and data modeling for easier refactoring and extension.

## Features

- **Accurate syllable counting** using the CMU Pronouncing Dictionary
- **Elision detection** for contractions like "o'er" and "you're"
- **Automatic title detection** (quoted, all-caps, or filename-matching)
- **Stanza structure analysis** with line and syllable counts per stanza
- **Batch processing** for multiple poem files
- **Fallback estimation** for words not in the CMU dictionary

## Installation

### Prerequisites

- Python 3.13.5 or higher
- Poetry (for dependency management)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Cerbers/oracle-of-the-abyss.git
cd oracle-of-the-abyss
```

2. Install dependencies:
```bash
poetry install
```

3. Download the CMU Pronouncing Dictionary:
```bash
python -m nltk.downloader cmudict
```

## Usage

### Basic Usage

Place your poem files (`.txt` format) in the `user poems` folder and run:

```bash
poetry run python -m oracle.main
```

This will generate analysis files for each poem with the suffix `_analysis.txt`.

### Programmatic Usage

```python
from pathlib import Path
from oracle.poem_model import Poem
from oracle.analyzer import analyze_poem

# Load a poem
poem_text = """Born out of the void
Amidst the stars of flesh
An illusion both full and empty"""

poem = Poem(text=poem_text, filepath=Path("example.txt"))

# Analyze it
analysis = analyze_poem(poem)

# Access results
print(analysis['syllables_per_line'])  # [[5, 6, 9]]
print(analysis['line_counts'])          # [3]
```

### Example Output

For a poem like:
```
Born out of the void
Amidst the stars of flesh
An illusion both full and empty
O'er the abyss' watchful maw

Gazes into the weary eyes of a lost stalker
```

Oracle generates:
```
Stanza 1:
Born out of the void
Amidst the stars of flesh
An illusion both full and empty
O'er the abyss' watchful maw
Lines: 4
Syllables per line: [5, 6, 9, 7]

Stanza 2:
Gazes into the weary eyes of a lost stalker
Lines: 1
Syllables per line: [13]
```

## Project Structure

```
oracle/  
├── domain_objects.py    # Core domain models (Word, Line, Stanza)
├── parser.py            # Text parsing into domain objects
├── syllable_counter.py  # Syllable counting logic
├── poem_model.py        # Poem dataclass with cached properties
├── analyzer.py          # Main analysis orchestration
├── utils.py             # Helper functions
└── main.py              # CLI entry point
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Project Principles

This project follows test-driven development (TDD) with:
- Comprehensive test coverage before implementation
- Maximum 1 level of inheritance
- Modular architecture over quick fixes

## Technical Details

### Syllable Counting Algorithm

1. Check CMU dictionary for exact word match
2. Try lowercase version
3. Detect and handle elisions (vowel + apostrophe + vowel)
4. Strip punctuation and retry
5. Fall back to vowel-group counting

### Handling Multiple Pronunciations

Words with multiple pronunciations in the CMU dictionary currently use the first (most common) variant. Future versions will explore all pronunciation combinations to identify consistent metrical patterns.

## Known Limitations

- **Whitespace handling:** Leading whitespace and indentation in poem files are stripped during parsing. This affects visual formatting in the analysis output but does not impact syllable counting.
- **Pronunciation variants:** The syllable counter currently uses the first pronunciation variant from the CMU dictionary, which may not always reflect the intended pronunciation in context. For example, "our" could be 2 syllables or 1 syllable

I'm aware of these limitations and will address them as the project continues.

## Roadmap

- [ ] Support for multiple pronunciation variants per word
- [ ] Pattern detection across stanzas (rhyme schemes, meter)
- [ ] CLI with arguments for custom folders and output formats
- [ ] Improved error handling and user feedback
- [ ] Performance optimization for large poem collections

## License

MIT License - see LICENSE file for details

## Contributing

This is a personal learning project, but suggestions and feedback are welcome! Feel free to open an issue to discuss potential improvements.

## Acknowledgments

- CMU Pronouncing Dictionary for phonetic data
- NLTK for dictionary access