from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.preferences import PreferencesCreate, PreferencesResponse, PreferencesUpdate
from app.services.preferences_service import preferences_service

router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.post("", response_model=PreferencesResponse, status_code=status.HTTP_201_CREATED)
def create_preferences(request: PreferencesCreate, current_user: dict = Depends(get_current_user)):
    try:
        preferences = preferences_service.create_preferences(current_user["id"], request.model_dump(mode="json", exclude_unset=True))
        return PreferencesResponse(**preferences)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("/me", response_model=PreferencesResponse)
def get_my_preferences(current_user: dict = Depends(get_current_user)):
    try:
        preferences = preferences_service.get_preferences(current_user["id"])
        return PreferencesResponse(**preferences)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.put("/me", response_model=PreferencesResponse)
def update_preferences(request: PreferencesUpdate, current_user: dict = Depends(get_current_user)):
    try:
        preferences = preferences_service.update_preferences(current_user["id"], request.model_dump(mode="json", exclude_unset=True))
        return PreferencesResponse(**preferences)
    except ValueError as error:
        error_status = (
            status.HTTP_400_BAD_REQUEST
            if "min_age" in str(error)
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=error_status, detail=str(error)) from error


@router.get("/discover", response_model=list)
def discover_profiles(current_user: dict = Depends(get_current_user)):
    return preferences_service.discover_profiles(current_user["id"])
