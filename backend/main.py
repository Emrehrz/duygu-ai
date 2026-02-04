from datetime import datetime
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from sentiment import SentimentEngine
from recommender import RecommendationEngine
from rate_limiter import is_rate_limited


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
    timestamp: Optional[str] = None


class ErrorResponse(BaseModel):
    code: str
    detail: str


class AnalyzeEnvelope(BaseModel):
    data: Optional[AnalyzeResponse] = None
    error: Optional[ErrorResponse] = None


class RecommendRequest(BaseModel):
    valence: float
    arousal: float


class Track(BaseModel):
    title: str
    artist: str
    score: float
    youtube_url: str


class RecommendResponse(BaseModel):
    tracks: List[Track]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# --- endpointler ---


@app.post("/analyze", response_model=AnalyzeEnvelope)
async def analyze_mood(request: Request, payload: AnalyzeRequest):
    """
    Kullanicinin metnini analiz eder ve duygu durumunu dondurur
    """
    client_ip = request.client.host

    text = payload.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    print(f"DEBUG: Gelen İstek -> Metin: {text}")

    if is_rate_limited(client_ip):
        return AnalyzeEnvelope(
            error=ErrorResponse(
                code="RATE_LIMITED",
                detail="Lütfen biraz bekle kendime geleyim.",
            )
        )

    # sentiment engine i cagir
    result = sentiment_engine.analyze(text)
    return AnalyzeEnvelope(data=AnalyzeResponse(**result))


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
