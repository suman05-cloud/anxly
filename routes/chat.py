from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.nvidia import stream_chat_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: list = []

@router.post("/chat")
def chat(req: ChatRequest):
    try:
        # ✅ Sanitize history — normalize roles, skip empty messages
        clean_history = []
        for msg in req.history:
            role    = msg.get("role", "")
            content = msg.get("content", "")
            if role not in ("user", "assistant", "system"):
                role = "assistant"
            if content.strip():
                clean_history.append({"role": role, "content": content})

        # ✅ Always append current user message last
        clean_history.append({"role": "user", "content": req.message})

        return StreamingResponse(
            stream_chat_response(clean_history),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",  # critical for Railway/nginx
                "Connection": "keep-alive",
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))