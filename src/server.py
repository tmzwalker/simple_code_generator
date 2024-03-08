import json
import uuid
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from generator import generate_code


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Store generated snippets and feedback
snippet_store = []
feedback_store = []

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
def generate(request: Request, model: str = Form(...), description: str = Form(...)):
    # Generate code snippet using the selected LLM model
    code_snippet = generate_code(description, model_name=model)

    # Store the generated snippet
    snippet_id = uuid.uuid4().__str__()
    snippet_store.append({
        "id": snippet_id,
        "description": description,
        "code_snippet": code_snippet
    })
    return templates.TemplateResponse("index.html", {"request": request, "code_snippet": code_snippet, "description": description, "model": model, "snippet_id": snippet_id, "snippets": snippet_store})

@app.post("/feedback")
def provide_feedback(request: Request, description: str = Form(...), code_snippet: str = Form(...), model: str = Form(...), feedback: str = Form(...), rating: str = Form(...)):
    # Store the feedback for future improvements
    feedback_store.append({
        "description": description,
        "code_snippet": code_snippet,
        "model_name": model,
        "feedback": feedback,
        "rating": rating
    })
    # Save feedback data for testing
    with open("feedback.json", "w") as file:
        json.dump(feedback_store, file, indent=4)

    return templates.TemplateResponse("index.html", {"request": request, "feedback_received": True, "snippets": snippet_store})

@app.post("/delete")
def delete_snippet(request: Request, snippet_id: str = Form(...)):
    # Remove the snippet from the store
    snippet_store[:] = [snippet for snippet in snippet_store if snippet["id"] != snippet_id]
    return templates.TemplateResponse("index.html", {"request": request, "snippets": snippet_store})
