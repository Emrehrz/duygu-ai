# Duygu AI - Backend

FastAPI backend for the AI chat application.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

- `GET /` - Welcome message and API info
- `POST /analyze` - Analyze user text and return emotion, valence, arousal, confidence, provider
- `POST /recommend` - Recommend music tracks based on valence and arousal values

- `GET /health` - Health check

```json
### Example: Analyze Endpoint

Request:
```json
{
  "text": "Bugün kendimi çok mutlu hissediyorum!"
}
```

Response:
```json
{
  "valence": 0.8,
  "arousal": 0.6,
  "emotion": "happy",
  "confidence": 0.3,
  "provider": "local"
}
```

### Example: Recommend Endpoint

Request:
```json
{
  "valence": 0.8,
  "arousal": 0.6
}
```

Response:
```json
{
  "tracks": [
    {"title": "Song 1", "artist": "Artist A", "score": 0.92},
    {"title": "Song 2", "artist": "Artist B", "score": 0.89}
  ]
}
```
```
