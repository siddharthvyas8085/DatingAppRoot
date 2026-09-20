from fastapi import APIRouter, Depends, HTTPException, status


from app.core.dependencies import get_current_user
from app.schemas.profile import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)
from app.services.profile_service import profile_service


router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    request: ProfileCreate,
    current_user: dict = Depends(get_current_user),
):

    try:

        profile = profile_service.create_profile(
            user_id=current_user["id"],
            profile_data=request.model_dump(
                mode="json"
            ),
        )

        return profile

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.get(
    "/me",
    response_model=ProfileResponse,
)
def get_my_profile(
    current_user: dict = Depends(get_current_user),
):

    try:

        return profile_service.get_profile(
            current_user["id"]
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.put(
    "/me",
    response_model=ProfileResponse,
)
def update_my_profile(
    request: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
):

    try:

        return profile_service.update_profile(
            user_id=current_user["id"],
            profile_data=request.model_dump(
                mode="json",
                exclude_unset=True,
            ),
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )