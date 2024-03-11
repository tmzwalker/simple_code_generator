import pytest  # noqa: F401
from fastapi.testclient import TestClient
from server import app, snippet_store, feedback_store

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Code Generation Web Interface" in response.text


def test_generate():
    description = "Generate a function to calculate the factorial of a number"
    model = "gpt-3.5-turbo"
    response = client.post("/generate", data={"description": description, "model": model})
    assert response.status_code == 200
    assert description in response.text


def test_evaluate():
    snippet_id = snippet_store[0]["id"]
    code_snippet = snippet_store[0]["code_snippet"]
    model = "gpt-3.5-turbo"
    response = client.post("/evaluate", data={"snippet_id": snippet_id, "code_snippet": code_snippet, "model": model})
    assert response.status_code == 200
    assert "Code Evaluation:" in response.text


def test_provide_feedback():
    description = snippet_store[0]["description"]
    code_snippet = snippet_store[0]["code_snippet"]
    feedback = "Great code snippet!"
    rating = "good"
    response = client.post(
        "/feedback",
        data={
            "description": description,
            "code_snippet": code_snippet,
            "model": "gpt-3.5-turbo",
            "feedback": feedback,
            "rating": rating,
        },
    )
    assert response.status_code == 200
    assert "Thank you for your feedback!" in response.text
    assert feedback_store[-1]["feedback"] == feedback
    assert feedback_store[-1]["rating"] == rating


def test_delete_snippet():
    snippet_id = snippet_store[0]["id"]
    response = client.post("/delete", data={"snippet_id": snippet_id})
    assert response.status_code == 200
    assert snippet_id not in [snippet["id"] for snippet in snippet_store]
