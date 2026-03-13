from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from googleapiclient.discovery import build
from textblob import TextBlob
from dotenv import load_dotenv
import os
import re

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("YouTube API key not found in .env file")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

app = FastAPI(title="YouTube Sentiment Analysis API")


class VideoRequest(BaseModel):
    video_url: str
    count: int


def extract_video_id(url):
    pattern = r"(?:v=|youtu\.be/)([^&]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")


def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, polarity


def fetch_comments(video_id, count):
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(count, 100),
            textFormat="plainText"
        )

        response = request.execute()

        comments_data = []

        if "items" not in response:
            raise HTTPException(status_code=404, detail="No comments found")

        for item in response["items"]:
            comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            sentiment, polarity = analyze_sentiment(comment_text)

            comments_data.append({
                "comment": comment_text,
                "sentiment": sentiment,
                "polarity_score": polarity
            })

        return comments_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def home():
    return {"message": "YouTube Sentiment Analysis API is running"}


@app.post("/fetch_comments/")
def get_comments(request: VideoRequest):
    video_id = extract_video_id(request.video_url)
    comments = fetch_comments(video_id, request.count)

    summary = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0
    }

    for item in comments:
        summary[item["sentiment"]] += 1

    return {
        "video_id": video_id,
        "total_comments_analyzed": len(comments),
        "sentiment_summary": summary,
        "comments": comments
    }