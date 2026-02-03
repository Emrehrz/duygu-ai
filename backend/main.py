from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
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
    timestamp: datetime = Field(default_factory=datetime.now)


class RecommendRequest(BaseModel):
    valence: float
    arousal: float


class Track(BaseModel):
    title: str
    artist: str
    score: float


class RecommendResponse(BaseModel):
    tracks: List[Track]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# --- endpointler ---


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_mood(request: AnalyzeRequest):
    """
    Kullanicinin metnini analiz eder ve duygu durumunu dondurur
    """

    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    print(f"DEBUG: Gelen İstek -> Metin: {request.text}")

    # sentiment engine i cagir
    result = sentiment_engine.analyze(request.text)

    return result


@app.post("/recommend", response_model=RecommendResponse)
async def recommend_music(request: RecommendRequest):
    # TERMINALDE GÖRMEK İÇİN:
    print(
        f"DEBUG: Gelen İstek -> Valence: {request.valence}, Arousal: {request.arousal}")

    songs = recommender_engine.recommend(
        target_valence=request.valence,
        target_arousal=request.arousal
    )
    # İlk 3 şarkının skorunu da yazdıralım
    for s in songs[:3]:
        print(
            f"   -> Öneri: {s['title']} (V:{s['valence']}, E:{s['energy']}) - Skor: {s['score']:.3f}")

    return {"tracks": songs}


@app.get("/")
async def root():
    return {"message": "Duygu AI Chat API"}
