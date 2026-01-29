"""
API module for the Oracle Poetry Analyzer.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from oracle.analyzer import analyze_poem
from oracle.poem_model import Poem

app = FastAPI(
    title="Oracle Poetry Analyzer API",
    description="Analyze poems for syllable counts and structure.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", # local dev
        "https://oracle-of-the-abyss.onrender.com" # Render dev test
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class PoemRequest(BaseModel):
    """
    Request model for poem analysis.
    
    Attributes:
        poem_text: The text of the poem to analyze.
        title: The title of the poem.
    """
    poem_text: str
    title: str = "Untitled"

class BatchPoemRequest(BaseModel):
    """
    Request model for batch poem analysis.
    
    Attributes:
        poems: List of poems to analyze.
    """
    poems: list[PoemRequest]

class PoemAnalysisResult(BaseModel):
    """
    Result model for poem analysis.
    
    Attributes:
        title: The title of the poem.
        analysis: The analysis of the poem.
        error: Error message if analysis failed.
    """
    title: str
    analysis: dict
    error: str | None = None



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
    
@app.post("/batch-analyze")
def batch_analyze_endpoint(request: BatchPoemRequest):
    """
    Analyze multiple poems in a single request.

    Args:
        request (BatchPoemRequest): The request containing the poems to analyze.

    Returns:
        dict: A dictionary containing:
            - results: List of results, one for each poem
            - total: Total number of poems analyzed
    """
    results = []

    for poem_request in request.poems:
        try:
            poem = Poem(
                text=poem_request.poem_text,
                filepath=Path(f"{poem_request.title}.txt")
            )
            analysis = analyze_poem(poem)
            results.append(PoemAnalysisResult(
                title=poem_request.title,
                analysis=analysis,
                error=None
            ))
        except Exception as e:
            results.append(PoemAnalysisResult(
                title=poem_request.title,
                analysis={},
                error=str(e)
            ))
    return {"results": results, "total": len(results)}

    
@app.get("/health")
def health_check():
    """Check if the API and its dependencies are running properly."""

    try:
        #Test that syllable counter is accessible
        from oracle.syllable_counter import count_syllables
        test_count = count_syllables("test")

        return {
            "status": "healthy",
            "syllable_counter": "operational",
            "cmu_dict": "loaded"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# Serve built frontend (dist folder from root)
# Underscore to stop pdoc from documenting this variable since it's absolute path
_DIST_DIR = Path(__file__).parent.parent / "dist" 


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Serve the built frontend from the dist directory.
    
    Args:
        full_path (str): The path to the file to serve.
    
    Returns:
        FileResponse: The file to serve.
    """
    dist_resolved = _DIST_DIR.resolve()
    file_path = (_DIST_DIR / full_path).resolve()
    
    # Security check: ensure we're not serving files outside dist
    if file_path.is_file() and str(file_path).startswith(str(dist_resolved)):
        return FileResponse(file_path)
    
    # SPA fallback: serve index.html
    index_path = dist_resolved / "index.html"
    if index_path.is_file():
        return FileResponse(index_path)
    
    return {"error": "Frontend not found"}