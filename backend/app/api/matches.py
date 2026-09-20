from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.services.match_service import match_service

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/like/{user_id}", status_code=status.HTTP_200_OK)
def like_user(user_id: str, current_user: dict = Depends(get_current_user)):
    try:
        return match_service.like_profile(current_user["id"], user_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("", status_code=status.HTTP_200_OK)
def list_matches(current_user: dict = Depends(get_current_user)):
    repository = __import__("app.repositories.factory", fromlist=["get_repository"]).get_repository()
    return repository.get_user_matches(current_user["id"])
