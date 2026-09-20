from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/messages", status_code=status.HTTP_201_CREATED)
def send_message(payload: dict, current_user: dict = Depends(get_current_user)):
    try:
        return chat_service.send_message(payload["match_id"], current_user["id"], payload["content"])
    except (KeyError, TypeError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("/messages/{match_id}")
def get_messages(match_id: str, current_user: dict = Depends(get_current_user)):
    try:
        return chat_service.get_messages_for_match(match_id, current_user["id"])
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error
