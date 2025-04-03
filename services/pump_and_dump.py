from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sentiment_data_path = os.path.join(BASE_DIR, "data", "stock_sentiments.csv")




# Load historical sentiment data (Assume it's stored in a CSV)
sentiment_data_path = "../data/stock_sentiments.csv"

class StockCheck(BaseModel):
    ticker: str

@router.post("/detect-pump-dump/")
def detect_pump_and_dump(stock: StockCheck):
    try:
        df = pd.read_csv(sentiment_data_path)

        # Filter by ticker
        stock_data = df[df['ticker'] == stock.ticker]

        if stock_data.empty:
            raise HTTPException(status_code=404, detail="Stock data not found")

        # Check if sentiment spikes are unnatural (basic rule: spike > 2x average)
        avg_sentiment = stock_data["sentiment_score"].mean()
        last_sentiment = stock_data["sentiment_score"].iloc[-1]

        if last_sentiment > 2 * avg_sentiment:
            return {"ticker": stock.ticker, "warning": "Possible Pump-and-Dump activity detected!"}
        
        return {"ticker": stock.ticker, "message": "No suspicious activity detected."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
