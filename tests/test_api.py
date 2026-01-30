import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from oracle.api import app, PoemRequest, BatchPoemRequest, PoemAnalysisResult


client = TestClient(app)


class TestAnalyzeEndpoint:
    """Tests for the /analyze endpoint."""

    def test_analyze_single_poem_valid_request(self):
        """Test analyzing a single poem with valid request data."""
        request_data = {
            "poem_text": "Born out of the void\nAmidst the stars of flesh\nAn illusion both full and empty",
            "title": "Test Poem"
        }
        
        response = client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "stanza_texts" in data
        assert "line_counts" in data
        assert "syllables_per_line" in data
        assert len(data["stanza_texts"]) > 0
        assert len(data["line_counts"]) > 0
        assert len(data["syllables_per_line"]) > 0

    def test_analyze_poem_with_default_title(self):
        """Test that poem analysis works with default title when not provided."""
        request_data = {
            "poem_text": "Roses are red\nViolets are blue"
        }
        
        response = client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "stanza_texts" in data

    def test_analyze_poem_with_multiple_stanzas(self):
        """Test analyzing a poem with multiple stanzas."""
        request_data = {
            "poem_text": "First stanza line one\nFirst stanza line two\n\nSecond stanza line one\nSecond stanza line two",
            "title": "Multi-Stanza"
        }
        
        response = client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["stanza_texts"]) == 2
        assert len(data["line_counts"]) == 2
        assert len(data["syllables_per_line"]) == 2

    def test_analyze_poem_empty_text_returns_400(self):
        """Test that empty poem text returns 400 Bad Request."""
        request_data = {
            "poem_text": "",
            "title": "Empty"
        }
        
        response = client.post("/analyze", json=request_data)
        
        assert response.status_code == 400
        assert "detail" in response.json()

    def test_analyze_poem_missing_poem_text_returns_422(self):
        """Test that missing required poem_text field returns 422 Unprocessable Entity."""
        request_data = {
            "title": "No Text"
        }
        
        response = client.post("/analyze", json=request_data)
        
        assert response.status_code == 422

    def test_analyze_poem_syllable_counts_are_integers(self):
        """Test that syllable counts are returned as integers."""
        request_data = {
            "poem_text": "Hello world\nTest line",
            "title": "Syllable Test"
        }
        
        response = client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        for stanza_syllables in data["syllables_per_line"]:
            for syllable_count in stanza_syllables:
                assert isinstance(syllable_count, int)
                assert syllable_count >= 0

    def test_analyze_poem_line_counts_match_stanza_texts(self):
        """Test that line counts match the actual number of lines in stanza texts."""
        request_data = {
            "poem_text": "Line one\nLine two\nLine three\n\nLine four",
            "title": "Count Test"
        }
        
        response = client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        for i, stanza_text in enumerate(data["stanza_texts"]):
            actual_line_count = len(stanza_text.strip().split("\n"))
            expected_line_count = data["line_counts"][i]
            assert actual_line_count == expected_line_count


class TestBatchAnalyzeEndpoint:
    """Tests for the /batch-analyze endpoint."""

    def test_batch_analyze_multiple_poems(self):
        """Test analyzing multiple poems in a single batch request."""
        request_data = {
            "poems": [
                {
                    "poem_text": "First poem line one\nFirst poem line two",
                    "title": "Poem One"
                },
                {
                    "poem_text": "Second poem line one\nSecond poem line two\nSecond poem line three",
                    "title": "Poem Two"
                }
            ]
        }
        
        response = client.post("/batch-analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total" in data
        assert data["total"] == 2
        assert len(data["results"]) == 2

    def test_batch_analyze_returns_correct_structure(self):
        """Test that batch results have the correct structure."""
        request_data = {
            "poems": [
                {
                    "poem_text": "Test poem",
                    "title": "Test"
                }
            ]
        }
        
        response = client.post("/batch-analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        result = data["results"][0]
        assert "title" in result
        assert "analysis" in result
        assert "error" in result
        assert result["error"] is None

    def test_batch_analyze_with_one_failing_poem(self):
        """Test that batch processing continues even if one poem fails."""
        request_data = {
            "poems": [
                {
                    "poem_text": "Valid poem line one\nValid poem line two",
                    "title": "Valid"
                },
                {
                    "poem_text": "",
                    "title": "Invalid"
                },
                {
                    "poem_text": "Another valid poem",
                    "title": "Also Valid"
                }
            ]
        }
        
        response = client.post("/batch-analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        
        valid_results = [r for r in data["results"] if r["error"] is None]
        invalid_results = [r for r in data["results"] if r["error"] is not None]
        
        assert len(valid_results) == 2
        assert len(invalid_results) == 1
        assert invalid_results[0]["title"] == "Invalid"

    def test_batch_analyze_empty_list(self):
        """Test batch analyze with an empty poems list."""
        request_data = {
            "poems": []
        }
        
        response = client.post("/batch-analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["results"]) == 0

    def test_batch_analyze_preserves_titles(self):
        """Test that batch results preserve the original poem titles."""
        titles = ["First", "Second", "Third"]
        request_data = {
            "poems": [
                {
                    "poem_text": f"Poem {title}",
                    "title": title
                }
                for title in titles
            ]
        }
        
        response = client.post("/batch-analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        result_titles = [r["title"] for r in data["results"]]
        assert result_titles == titles


class TestHealthCheckEndpoint:
    """Tests for the /health endpoint."""

    def test_health_check_returns_200(self):
        """Test that health check endpoint returns 200 OK."""
        response = client.get("/health")
        
        assert response.status_code == 200

    def test_health_check_returns_status_field(self):
        """Test that health check returns a status field."""
        response = client.get("/health")
        
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "unhealthy"]

    def test_health_check_returns_syllable_counter_status(self):
        """Test that health check includes syllable counter status."""
        response = client.get("/health")
        
        data = response.json()
        if data["status"] == "healthy":
            assert "syllable_counter" in data
            assert data["syllable_counter"] == "operational"
            assert "cmu_dict" in data
            assert data["cmu_dict"] == "loaded"


class TestPoemRequestModel:
    """Tests for the PoemRequest Pydantic model."""

    def test_poem_request_creation_with_all_fields(self):
        """Test creating a PoemRequest with all fields."""
        request = PoemRequest(
            poem_text="Test poem",
            title="Test Title"
        )
        
        assert request.poem_text == "Test poem"
        assert request.title == "Test Title"

    def test_poem_request_creation_with_default_title(self):
        """Test that PoemRequest uses default title when not provided."""
        request = PoemRequest(poem_text="Test poem")
        
        assert request.poem_text == "Test poem"
        assert request.title == "Untitled"

    def test_poem_request_validation_fails_without_poem_text(self):
        """Test that PoemRequest validation fails without poem_text."""
        with pytest.raises(ValueError):
            PoemRequest(title="No Text")


class TestBatchPoemRequestModel:
    """Tests for the BatchPoemRequest Pydantic model."""

    def test_batch_poem_request_creation(self):
        """Test creating a BatchPoemRequest with multiple poems."""
        request = BatchPoemRequest(
            poems=[
                PoemRequest(poem_text="Poem one", title="First"),
                PoemRequest(poem_text="Poem two", title="Second")
            ]
        )
        
        assert len(request.poems) == 2
        assert request.poems[0].title == "First"
        assert request.poems[1].title == "Second"

    def test_batch_poem_request_empty_list(self):
        """Test creating a BatchPoemRequest with empty poems list."""
        request = BatchPoemRequest(poems=[])
        
        assert len(request.poems) == 0


class TestPoemAnalysisResultModel:
    """Tests for the PoemAnalysisResult Pydantic model."""

    def test_poem_analysis_result_successful(self):
        """Test creating a successful PoemAnalysisResult."""
        result = PoemAnalysisResult(
            title="Test",
            analysis={"stanza_texts": [], "line_counts": [], "syllables_per_line": []},
            error=None
        )
        
        assert result.title == "Test"
        assert result.analysis == {"stanza_texts": [], "line_counts": [], "syllables_per_line": []}
        assert result.error is None

    def test_poem_analysis_result_with_error(self):
        """Test creating a PoemAnalysisResult with an error."""
        result = PoemAnalysisResult(
            title="Failed",
            analysis={},
            error="Analysis failed"
        )
        
        assert result.title == "Failed"
        assert result.error == "Analysis failed"

    def test_poem_analysis_result_error_defaults_to_none(self):
        """Test that error field defaults to None."""
        result = PoemAnalysisResult(
            title="Test",
            analysis={}
        )
        
        assert result.error is None


class TestAPIIntegration:
    """Integration tests for the API."""

    def test_analyze_and_batch_analyze_return_same_structure(self):
        """Test that single and batch endpoints return compatible structures."""
        poem_data = {
            "poem_text": "Integration test poem\nWith multiple lines",
            "title": "Integration"
        }
        
        single_response = client.post("/analyze", json=poem_data)
        batch_response = client.post("/batch-analyze", json={"poems": [poem_data]})
        
        assert single_response.status_code == 200
        assert batch_response.status_code == 200
        
        single_data = single_response.json()
        batch_data = batch_response.json()["results"][0]["analysis"]
        
        assert single_data == batch_data

    def test_real_poem_analysis(self):
        """Test analyzing a real poem with known structure."""
        poem_text = """"Voidborn"
Born out of the void
Amidst the stars of flesh
An illusion both full and empty
O'er the abyss' watchful maw

Gazes into the weary eyes of a lost stalker
Who lies in blood-flow of the night"""
        
        request_data = {
            "poem_text": poem_text,
            "title": "Voidborn"
        }
        
        response = client.post("/analyze", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["stanza_texts"]) == 2
        assert data["line_counts"] == [4, 2]
