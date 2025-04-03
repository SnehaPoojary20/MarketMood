from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_config import db  # Import Firebase Firestore

router = APIRouter()

# Define the data model
class SentimentData(BaseModel):
    text: str
    sentiment: str

@router.post("/store-sentiment/")
def store_sentiment(data: SentimentData):
    try:
        # Add data to Firestore
        doc_ref = db.collection("stock_sentiments").add(data.dict())
        
        return {"message": "Sentiment stored successfully!", "id": doc_ref[1].id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


