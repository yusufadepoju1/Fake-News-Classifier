from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from .predict import FakeNewsPredictor

app = FastAPI(title="Fake News Classifier")

# Set up static files and templates
base_dir = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Load predictor
# Predictor will be loaded on first request to save startup time, or global
try:
    predictor = FakeNewsPredictor()
except Exception as e:
    print(f"Warning: Model not found. ({e}) Please train the model first by running train.py")
    predictor = None

class PredictionRequest(BaseModel):
    title: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/predict")
async def predict_news(request: PredictionRequest):
    if predictor is None:
        return JSONResponse(status_code=500, content={"error": "Model not trained yet."})
    
    title = request.title
    if not title.strip():
        return JSONResponse(status_code=400, content={"error": "Title cannot be empty."})
        
    try:
        is_fake, confidence = predictor.predict(title)
        return {"is_fake": is_fake, "confidence": confidence}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
