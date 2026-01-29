# Oracle of the Abyss

A full-stack poetry analysis application that counts syllables and identifies structural patterns in poems. Features a FastAPI backend and React frontend.

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
- **REST API** for programmatic access
- **Web interface** for interactive poem analysis

## Installation

### Prerequisites

- Python 3.13 or higher
- Poetry (for dependency management)
- Node.js 20+ (for frontend development)

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Cerbers/oracle-of-the-abyss.git
cd oracle-of-the-abyss
```

2. Install Python dependencies:
```bash
poetry install
```

3. Download the CMU Pronouncing Dictionary:
```bash
python -m nltk.downloader cmudict
```

### Frontend Setup

```bash
cd frontend
npm install
```

## Usage

### Running as a Server

Start the FastAPI backend server:

```bash
uvicorn oracle.api:app --reload
```

The API will be available at `http://localhost:8000`.

To run with the frontend in development mode, open a second terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### Running with Docker

Build and run the complete application:

```bash
docker build -t oracle .
docker run -p 8000:8000 oracle
```

This serves both the API and frontend at `http://localhost:8000`.

### CLI Usage

Place your poem files (`.txt` or `.md` format) in the `user poems` folder and run:
```bash
poetry run python -m oracle.main
```

This will generate analysis files for each poem with the suffix `_analysis.txt`.

Additionally you can specify a folder to read poems from:
```bash
poetry run python -m oracle.main --folder "insert absolute or relative path"
```

**Performance monitoring:**
```bash
poetry run python -m oracle.main --perf
```


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

## API

The REST API provides programmatic access to poem analysis.

### Endpoints

#### `POST /analyze`

Analyze a single poem.

**Request:**
```json
{
  "poem_text": "Born out of the void\nAmidst the stars of flesh",
  "title": "My Poem"
}
```

**Response:**
```json
{
  "stanza_texts": ["Born out of the void\nAmidst the stars of flesh"],
  "line_counts": [2],
  "syllables_per_line": [[5, 6]]
}
```

#### `POST /batch-analyze`

Analyze multiple poems in one request.

**Request:**
```json
{
  "poems": [
    {"poem_text": "...", "title": "Poem 1"},
    {"poem_text": "...", "title": "Poem 2"}
  ]
}
```

**Response:**
```json
{
  "results": [
    {"title": "Poem 1", "analysis": {...}, "error": null},
    {"title": "Poem 2", "analysis": {...}, "error": null}
  ],
  "total": 2
}
```

#### `GET /health`

Health check for the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "syllable_counter": "operational",
  "cmu_dict": "loaded"
}
```

## Frontend

The web interface provides an interactive way to analyze poems.

### Features

- **Poem input form** with title and text fields
- **Real-time analysis** via API integration
- **Formatted output** displaying stanza structure and syllable counts
- **Responsive design** using Tailwind CSS

### Technology Stack

- React 19
- Vite (build tool)
- Tailwind CSS (styling)
- Axios (HTTP client)

### Environment Configuration

The frontend uses environment variables for API configuration:

- `.env` (development): `VITE_API_URL=http://localhost:8000`
- `.env.production` (production): `VITE_API_URL=https://oracle-of-the-abyss.onrender.com`

## Project Structure

```
oracle-of-the-abyss/
├── oracle/                      # Python backend
│   ├── api.py                   # FastAPI application & REST endpoints
│   ├── analyzer.py              # Main analysis orchestration
│   ├── poem_model.py            # Poem dataclass with cached properties
│   ├── parser.py                # Text parsing into domain objects
│   ├── domain_objects.py        # Core domain models (Word, Line, Stanza)
│   ├── syllable_counter.py      # Syllable counting logic
│   ├── utils.py                 # Helper functions
│   ├── main.py                  # CLI entry point
│   └── intern/
│       └── lookout.py           # Performance monitoring
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── App.jsx              # Main app component
│   │   ├── main.jsx             # React entry point
│   │   └── components/
│   │       ├── UserInputBox.jsx      # Poem input form
│   │       └── AnalysisOutputBox.jsx # Results display
│   ├── vite.config.js           # Vite configuration
│   └── package.json             # Node dependencies
├── tests/                       # Test suite
├── docs/                        # Documentation
├── user poems/                  # Sample poem files
├── Dockerfile                   # Multi-stage Docker build
├── render.yaml                  # Render deployment config
└── pyproject.toml               # Python project metadata
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Project Principles

This project emphasizes correctness, clarity, and incremental design.
Testing is used as a safety net and as executable documentation of expected behavior, rather than strict test-first development in all areas.

- Tests are added when behavior becomes clear and stable
- Exploratory implementation may precede tests for heuristic or algorithmic components
- Architecture favors modular design and explicit domain objects over quick fixes
- Inheritance is kept shallow (maximum one level) in favor of composition

## Technical Details

### Syllable Counting Algorithm

1. Check CMU dictionary for exact word match
2. Try lowercase version
3. Detect and handle elisions (vowel + apostrophe + vowel)
4. Strip punctuation and retry
5. Fall back to vowel-group counting

### Handling Multiple Pronunciations

Words with multiple pronunciations in the CMU dictionary currently use the first (most common) variant. Future versions will explore all pronunciation combinations to identify consistent metrical patterns.

## Deployment

The application is deployed on [Render](https://oracle-of-the-abyss.onrender.com).

### Deployment Configuration

The `render.yaml` file configures automatic deployment:

```yaml
services:
  - type: web
    name: oracle-api
    runtime: docker
    envVars:
      - key: PORT
        value: 10000
```

The Dockerfile uses a multi-stage build:
1. Stage 1 (Node.js): Builds the React frontend
2. Stage 2 (Python): Runs FastAPI and serves the built frontend

## Known Limitations

- **Whitespace handling:** Leading whitespace and indentation in poem files are stripped during parsing. This affects visual formatting in the analysis output but does not impact syllable counting.
- **Pronunciation variants:** The syllable counter currently uses the first pronunciation variant from the CMU dictionary, which may not always reflect the intended pronunciation in context. For example, "our" could be 2 syllables or 1 syllable.

I'm aware of these limitations and will address them as the project continues.

## Roadmap

- [ ] Support for multiple pronunciation variants per word
- [ ] Pattern detection across stanzas (rhyme schemes, meter)
- [ partially ] CLI with arguments for custom folders and output formats
- [ ] Improved error handling and user feedback
- [ ] Performance optimization for large poem collections

## License

MIT License - see LICENSE file for details

## Contributing

This is a personal learning project, but suggestions and feedback are welcome! Feel free to open an issue to discuss potential improvements.

## Acknowledgments

- CMU Pronouncing Dictionary for phonetic data
- NLTK for dictionary access