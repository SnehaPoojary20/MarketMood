from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

# Directly define API key (Replace with your actual key)
NEWS_API_KEY = "2d1477b7face45649e6495a2501b37a4"
NEWS_API_URL = f"https://newsapi.org/v2/everything?q=stock+market&language=en&apiKey={NEWS_API_KEY}"

@router.get("/fetch-news/")
def fetch_news():
    try:
        response = requests.get(NEWS_API_URL)
        news_data = response.json()

        if "articles" not in news_data:
            raise HTTPException(status_code=500, detail="Error fetching news")

        return {"top_news": news_data["articles"][:5]}  # Return top 5 articles
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

