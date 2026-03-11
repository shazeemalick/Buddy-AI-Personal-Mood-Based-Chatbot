from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import List, Optional
from pydantic import BaseModel

from database import engine, create_db_and_tables, get_session, add_message, get_chat_history, ChatMessage
from llm_service import generate_mood_response, MOOD_PROMPTS, analyze_mood, generate_summary

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Personal Mood-Based Chatbot API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.2f}s")
    return response

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    mood: str
    message: str

class MessageResponse(BaseModel):
    role: str
    content: str
    mood: str
    summary: Optional[str] = None
    detected_mood: Optional[str] = None

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/moods")
def get_moods():
    return list(MOOD_PROMPTS.keys())

@app.get("/history/{user_id}", response_model=List[MessageResponse])
def get_user_history(user_id: str, session: Session = Depends(get_session)):
    messages = get_chat_history(session, user_id)
    return [MessageResponse(role=m.role, content=m.content, mood=m.mood) for m in messages]

@app.post("/analyze_mood")
def analyze_mood_endpoint(request: ChatRequest):
    detected = analyze_mood(request.message)
    return {"detected_mood": detected}

@app.post("/chat", response_model=MessageResponse)
async def chat_endpoint(request: ChatRequest, session: Session = Depends(get_session)):
    history_objs = get_chat_history(session, request.user_id)
    history_data = [{"role": m.role, "content": m.content} for m in history_objs]
    
    # 1. Add user message
    user_msg = ChatMessage(user_id=request.user_id, mood=request.mood, role="user", content=request.message)
    add_message(session, user_msg)
    
    # 2. Generate response
    try:
        response_text = generate_mood_response(request.mood, request.message, history_data)
        
        # 3. Optional: Auto-detect mood for next time
        detected_mood = analyze_mood(request.message)
        
        # 4. Optional: Generate summary if history is long enough (e.g., every 6 messages)
        summary = None
        if len(history_objs) > 0 and (len(history_objs) + 2) % 6 == 0:
            summary = generate_summary(history_data + [{"role": "user", "content": request.message}])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # 5. Add assistant response
    assistant_msg = ChatMessage(user_id=request.user_id, mood=request.mood, role="assistant", content=response_text)
    add_message(session, assistant_msg)
    
    return MessageResponse(
        role="assistant", 
        content=response_text, 
        mood=request.mood,
        summary=summary,
        detected_mood=detected_mood
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
