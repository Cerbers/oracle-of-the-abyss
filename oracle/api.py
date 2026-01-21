from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from oracle.analyzer import analyze_poem
from oracle.poem_model import Poem

app = FastAPI(
    title="Oracle Poetry Analyzer API",
    description="Analyze poems for syllable counts and structure.",
    version="0.1.0"
)

class PoemRequest(BaseModel):
    poem_text: str
    title: str = "Untitled"


@app.get("/")
def root():
    return {
        "message": "Oracle API is running",
        "version": "0.1.0",
        "endpoints": ["/analyze", "/docs"]
    }

@app.post("/analyze")
def analyze_endpoint(request: PoemRequest):
    """
    Analyze a poem and return syllable counts per stanza.

    Returns:
    - stanza_texts: List of stanza contents
    - line_counts: Number of lines per stanza
    - syllables_per_line: Syllable counts for each line in each stanza
    """

    try:
        poem = Poem(
            text=request.poem_text,
            filepath=Path(f"{request.title}.txt")
        )
        result = analyze_poem(poem)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")