from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime

app = FastAPI(title="Duygu AI Chat API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str
    timestamp: str = None

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []

class ChatResponse(BaseModel):
    message: str
    timestamp: str

# Mock AI responses for demo purposes
AI_RESPONSES = [
    "That's an interesting question! Let me help you with that.",
    "I understand what you're asking. Here's what I think...",
    "Great point! Based on what you've said, I'd suggest...",
    "I'm here to help! Let me provide some insights on that.",
    "That's a thoughtful question. Let me break it down for you.",
    "I appreciate you sharing that. Here's my perspective...",
    "Interesting! I've processed your message and here's what I found...",
    "Thanks for asking! I'd be happy to discuss that with you.",
]

@app.get("/")
async def root():
    return {
        "message": "Welcome to Duygu AI Chat API",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - Send a message and get AI response",
            "/health": "GET - Check API health"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return an AI response
    """
    # For demo purposes, we'll return a random response
    # In a real application, this would call an actual AI model
    ai_response = random.choice(AI_RESPONSES)
    
    # Add some context based on the user's message
    if "hello" in request.message.lower() or "hi" in request.message.lower():
        ai_response = "Hello! I'm Duygu AI. How can I assist you today?"
    elif "bye" in request.message.lower() or "goodbye" in request.message.lower():
        ai_response = "Goodbye! It was nice chatting with you. Feel free to come back anytime!"
    elif "?" in request.message:
        ai_response = f"That's a great question! {random.choice(AI_RESPONSES)}"
    elif "help" in request.message.lower():
        ai_response = "I'm here to help! You can ask me anything, and I'll do my best to assist you."
    elif "thanks" in request.message.lower() or "thank you" in request.message.lower():
        ai_response = "You're welcome! Happy to help!"
    
    return ChatResponse(
        message=ai_response,
        timestamp=datetime.now().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
