import os
import joblib
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Get the absolute path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "data", "fake_news_model.pkl")

# Load model
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise RuntimeError(f"❌ Model file not found at {MODEL_PATH}. Please train it first.")
except Exception as e:
    raise RuntimeError(f"⚠️ Error loading model: {e}")

@router.post("/predict-fake-news/")
def predict_fake_news(article: str):
    try:
        prediction = model.predict([article])
        return {"fake_news_prediction": bool(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

