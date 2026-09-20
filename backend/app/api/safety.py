from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.services.safety_service import safety_service

router = APIRouter(prefix="/safety", tags=["Safety"])


@router.post("/block", status_code=status.HTTP_201_CREATED)
def block_user(payload: dict, current_user: dict = Depends(get_current_user)):
    try:
        return safety_service.block_user(current_user["id"], payload["user_id"])
    except (KeyError, TypeError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.post("/report", status_code=status.HTTP_201_CREATED)
def report_user(payload: dict, current_user: dict = Depends(get_current_user)):
    try:
        return safety_service.report_user(current_user["id"], payload["user_id"], payload["reason"])
    except (KeyError, TypeError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.post("/unmatch")
def unmatch_users(payload: dict, current_user: dict = Depends(get_current_user)):
    try:
        return safety_service.unmatch_users(current_user["id"], payload["user_id"])
    except (KeyError, TypeError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
