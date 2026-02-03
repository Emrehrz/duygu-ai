from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentiment import SentimentEngine
from recommender import RecommendationEngine

app = FastAPI(title="Duygu AI Chat API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# motorlari baslat
sentiment_engine = SentimentEngine()
recommender_engine = RecommendationEngine()

# modeller


class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    valence: float
    arousal: float
    emotion: str
    confidence: float
    provider: str


class RecommendRequest(BaseModel):
    valence: float
    arousal: float


class Track(BaseModel):
    title: str
    artist: str
    score: float


class RecommendResponse(BaseModel):
    tracks: List[Track]

# --- endpointler ---


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_mood(request: AnalyzeRequest):
    """
    Kullanicinin metnini analiz eder ve duygu durumunu dondurur
    """

    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # sentiment engine i cagir
    result = sentiment_engine.analyze(request.text)

    return result


@app.post("/recommend", response_model=RecommendResponse)
async def recommend_music(request: RecommendRequest):
    """
    valence ve arousal degerlerine gore muzik onerir
    """
    songs = recommender_engine.recommend(
        target_valence=request.valence,
        target_arousal=request.arousal
    )
    return {"tracks": songs}


@app.get("/")
async def root():
    return {"message": "Duygu AI Chat API"}
