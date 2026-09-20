from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.services.ai_service import ai_service

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/message-suggestions")
def get_message_suggestions(payload: dict, current_user: dict = Depends(get_current_user)):
    history = payload.get("history", [])
    if not isinstance(history, list):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="history must be a list")

    return {
        "user_id": current_user["id"],
        "suggestions": ai_service.generate_message_suggestions(history, current_user["id"]),
    }
