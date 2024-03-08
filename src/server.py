from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from generator import generate_code


app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Store feedback for future improvements
feedback_store = []

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
def generate(request: Request, model: str = Form(...), description: str = Form(...)):
    # Generate code snippet using the selected LLM model
    code_snippet = generate_code(description, model_name=model)
    return templates.TemplateResponse("index.html", {"request": request, "code_snippet": code_snippet, "description": description})

@app.post("/feedback")
def provide_feedback(request: Request, description: str = Form(...), code_snippet: str = Form(...), feedback: str = Form(...), rating: str = Form(...)):
    # Store the feedback for future improvements
    feedback_store.append({
        "description": description,
        "code_snippet": code_snippet,
        "feedback": feedback,
        "rating": rating
    })
    return templates.TemplateResponse("index.html", {"request": request, "feedback_received": True})