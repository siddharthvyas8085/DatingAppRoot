# from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)

from app.services.auth_service import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(request: RegisterRequest):

    try:

        user = auth_service.register_user(
            email=request.email,
            password=request.password,
        )

        return RegisterResponse(
            id=user["id"],
            email=user["email"],
            message="Registration successful",
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(request: LoginRequest):

    try:

        result = auth_service.login_user(
            email=request.email,
            password=request.password,
        )

        return LoginResponse(
            id=result["id"],
            email=result["email"],
            access_token=result["access_token"],
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )


@router.get("/me")
def get_me(
    current_user: dict = Depends(get_current_user),
):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
    }