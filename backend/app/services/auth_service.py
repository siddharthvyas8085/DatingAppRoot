from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.core.supabase_auth import (
    is_supabase_auth_enabled,
    sign_in_with_supabase,
    sign_up_with_supabase,
)
from app.repositories.factory import get_repository

repository = get_repository()


class AuthService:

    def register_user(
        self,
        email: str,
        password: str,
    ):

        if is_supabase_auth_enabled():
            return sign_up_with_supabase(email, password)

        existing_user = repository.get_user_by_email(
            email
        )

        if existing_user:
            raise ValueError(
                "Email already registered"
            )

        password_hash = hash_password(password)

        user = repository.create_user(
            email=email,
            password_hash=password_hash,
        )

        return user

    def login_user(
        self,
        email: str,
        password: str,
    ):

        if is_supabase_auth_enabled():
            return sign_in_with_supabase(email, password)

        user = repository.get_user_by_email(
            email
        )

        if not user:
            raise ValueError(
                "Invalid email or password"
            )

        password_valid = verify_password(
            password,
            user["password_hash"],
        )

        if not password_valid:
            raise ValueError(
                "Invalid email or password"
            )

        access_token = create_access_token(
            user["id"]
        )

        return {
            "id": user["id"],
            "email": user["email"],
            "access_token": access_token,
        }


auth_service = AuthService()