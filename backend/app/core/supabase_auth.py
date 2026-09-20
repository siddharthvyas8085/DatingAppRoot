import os

from dotenv import load_dotenv
from supabase import create_client


load_dotenv()


def is_supabase_auth_enabled() -> bool:
    value = os.getenv("USE_SUPABASE", "false").strip().lower()
    return value in {"1", "true", "yes", "on"}


def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Supabase Auth is enabled but SUPABASE_URL/SUPABASE_KEY are missing")

    return create_client(url, key)


def sign_up_with_supabase(email: str, password: str):
    client = get_supabase_client()
    response = client.auth.sign_up({
        "email": email,
        "password": password,
    })

    user = getattr(response, "user", None)
    if user is None and hasattr(response, "get"):
        user = response.get("user")

    if user is None:
        raise ValueError("Supabase signup failed")

    return {
        "id": user.id,
        "email": user.email,
    }


def sign_in_with_supabase(email: str, password: str):
    client = get_supabase_client()
    response = client.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })

    session = getattr(response, "session", None)
    user = getattr(response, "user", None)

    if session is None and hasattr(response, "get"):
        session = response.get("session")

    if user is None and hasattr(response, "get"):
        user = response.get("user")

    if session is None or user is None:
        raise ValueError("Invalid email or password")

    return {
        "id": user.id,
        "email": user.email,
        "access_token": session.access_token,
    }


def get_user_from_supabase_token(access_token: str):
    client = get_supabase_client()
    response = client.auth.get_user(access_token)

    user = getattr(response, "user", None)
    if user is None and hasattr(response, "get"):
        user = response.get("user")

    if user is None:
        raise ValueError("User not found")

    return {
        "id": user.id,
        "email": user.email,
    }
