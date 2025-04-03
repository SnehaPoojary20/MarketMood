from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import firebase_admin
from firebase_admin import credentials, firestore
import base64
from io import BytesIO
import os
import joblib
from pydantic import BaseModel
from services.fake_news_detector import router as fake_news_router
from services.pump_and_dump import router as pump_dump_router
from services.news_fetcher import router as news_router

app = FastAPI()

# Allow requests from React frontend
origins = [
    "http://localhost:5173",  # Vite React
    "http://localhost:3000"   # Create React App (if used)
]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(fake_news_router)
app.include_router(pump_dump_router)
app.include_router(news_router)

# Initialize Firebase
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
cred_path = os.path.join(BASE_DIR, "marketmood.json")

if not firebase_admin._apps:  # Prevent re-initialization error
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
COLLECTION_ID = "stock_sentiments"

# Load Trained Model
MODEL_PATH = os.path.join(BASE_DIR, "services", "data", "fake_news_model.pkl")
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

# Define Request Model
class NewsRequest(BaseModel):
    text: str

# Generate Pie Chart
def generate_pie_chart(sentiment_counts):
    labels = list(sentiment_counts.keys())
    sizes = list(sentiment_counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['green', 'red', 'gray'])
    plt.title("Sentiment Distribution")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()
    return encoded_image

# Generate Bar Chart
def generate_bar_chart(sentiment_counts):
    plt.figure(figsize=(6, 4))
    sns.barplot(x=list(sentiment_counts.keys()), y=list(sentiment_counts.values()), palette=['green', 'red', 'gray'])
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.title("Sentiment Count Bar Chart")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()
    return encoded_image

# API Endpoint: Upload Cleaned Data
@app.post("/upload/cleaned-data/")
async def upload_cleaned_data(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        # Validate CSV Columns
        required_columns = ["Link", "Text", "Sentiment", "Date"]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail="CSV file must contain 'Link', 'Text', 'Sentiment', and 'Date' columns")

        # Save Data
        save_path = os.path.join(BASE_DIR, "cleaned_data.csv")
        df.to_csv(save_path, index=False)

        # Upload to Firebase
        for _, row in df.iterrows():
            db.collection(COLLECTION_ID).add({
                "Link": row["Link"],
                "Text": row["Text"],
                "Sentiment": row["Sentiment"],
                "Date": row["Date"]
            })

        # Generate Charts
        sentiment_counts = df["Sentiment"].value_counts().to_dict()
        pie_chart = generate_pie_chart(sentiment_counts)
        bar_chart = generate_bar_chart(sentiment_counts)

        return {
            "message": "✅ Cleaned dataset saved and uploaded to Firebase!",
            "file_path": save_path,
            "sentiment_counts": sentiment_counts,
            "pie_chart": pie_chart,
            "bar_chart": bar_chart
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoint: Fake News Prediction
@app.post("/predict")
async def predict_news(news: NewsRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    prediction = model.predict([news.text])[0]
    label = "Fake News" if prediction == 1 else "Real News"
    return {"prediction": label}

# API Endpoint: Sentiment Analysis (Fix for 404 Error)
@app.get("/get-sentiment")
async def get_sentiment():
    try:
        docs = db.collection(COLLECTION_ID).stream()
        sentiments = [doc.to_dict() for doc in docs]
        return {"sentiments": sentiments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoint: Image Upload for Sentiment Analysis
@app.post("/analyze/image/")
async def analyze_image(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        print("Received Image:", file.filename)
        return {"message": "Image received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))










