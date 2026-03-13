YouTube Sentiment Analysis API

A FastAPI-based backend application that extracts comments from a YouTube video and performs sentiment analysis on them using TextBlob. The API returns individual comment sentiments along with an overall sentiment summary.

Features

Extract comments from any public YouTube video

Perform sentiment analysis (Positive, Negative, Neutral)

Return polarity scores for each comment

Provide overall sentiment summary

Built using FastAPI for fast API performance

Technologies Used

Python

FastAPI

TextBlob

YouTube Data API v3

Pydantic

python-dotenv

Project Structure
youtube-sentiment-analysis
│
├── main.py
├── .env
├── requirements.txt
└── README.md
Installation
1. Clone the Repository
git clone https://github.com/your-username/youtube-sentiment-analysis.git
cd youtube-sentiment-analysis
2. Create Virtual Environment
python -m venv venv

Activate it

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
Setup Environment Variables

Create a .env file in the project root.

YOUTUBE_API_KEY=your_youtube_api_key_here

To generate an API key:

Go to Google Cloud Console

Enable YouTube Data API v3

Create API credentials

Copy the API key

Running the API

Start the FastAPI server

uvicorn main:app --reload

Server will run at

http://127.0.0.1:8000
API Endpoints
Home Endpoint
GET /

Response

{
  "message": "YouTube Sentiment Analysis API is running"
}
Fetch Comments and Analyze Sentiment
POST /fetch_comments/

Request Body

{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "count": 20
}
Example Response
{
  "video_id": "VIDEO_ID",
  "total_comments_analyzed": 20,
  "sentiment_summary": {
    "Positive": 12,
    "Negative": 3,
    "Neutral": 5
  },
  "comments": [
    {
      "comment": "This video is amazing!",
      "sentiment": "Positive",
      "polarity_score": 0.8
    }
  ]
}
Testing the API

Open FastAPI interactive docs:

http://127.0.0.1:8000/docs

You can test endpoints directly from the Swagger UI.

Requirements

Example requirements.txt

fastapi
uvicorn
google-api-python-client
textblob
python-dotenv
pydantic
How It Works

The API receives a YouTube video URL and comment count.

The video ID is extracted from the URL.

The YouTube Data API fetches comments.

Each comment is analyzed using TextBlob sentiment polarity.

Sentiments are categorized into Positive, Negative, or Neutral.

The API returns comment sentiments and a summary.

Future Improvements

Add graphical sentiment visualization

Support pagination for large comment datasets

Store results in a database

Add frontend dashboard
