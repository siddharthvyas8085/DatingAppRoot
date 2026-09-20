import os
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


class SupabaseRepository:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url:
            raise ValueError("SUPABASE_URL is not configured")

        if not key:
            raise ValueError("SUPABASE_KEY is not configured")

        self.client: Client = create_client(url, key)

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    # -------------------------
    # USERS
    # -------------------------

    def create_user(
        self,
        email: str,
        password_hash: str,
    ):
        user_id = str(__import__("uuid").uuid4())

        data = {
            "id": user_id,
            "email": email,
            "password_hash": password_hash,
            "created_at": self._now(),
        }

        response = (
            self.client
            .table("users")
            .insert(data)
            .execute()
        )

        return response.data[0]

    def get_user_by_email(
        self,
        email: str,
    ) -> Optional[dict]:

        response = (
            self.client
            .table("users")
            .select("*")
            .eq("email", email)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    def get_user_by_id(
        self,
        user_id: str,
    ) -> Optional[dict]:

        response = (
            self.client
            .table("users")
            .select("*")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    # -------------------------
    # PROFILES
    # -------------------------

    def create_profile(self, profile: dict):

        response = (
            self.client
            .table("profiles")
            .insert(profile)
            .execute()
        )

        return response.data[0]

    def get_profile(
        self,
        user_id: str,
    ) -> Optional[dict]:

        response = (
            self.client
            .table("profiles")
            .select("*")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    def get_all_profiles(self):

        response = (
            self.client
            .table("profiles")
            .select("*")
            .execute()
        )

        return response.data

    def update_profile(
        self,
        user_id: str,
        updates: dict,
    ):

        updates["updated_at"] = self._now()

        response = (
            self.client
            .table("profiles")
            .update(updates)
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    # -------------------------
    # PREFERENCES
    # -------------------------

    def create_preferences(
        self,
        preferences: dict,
    ):

        response = (
            self.client
            .table("preferences")
            .insert(preferences)
            .execute()
        )

        return response.data[0]

    def get_preferences(
        self,
        user_id: str,
    ) -> Optional[dict]:

        response = (
            self.client
            .table("preferences")
            .select("*")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    def update_preferences(
        self,
        user_id: str,
        updates: dict,
    ):

        updates["updated_at"] = self._now()

        response = (
            self.client
            .table("preferences")
            .update(updates)
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    # -------------------------
    # LIKES
    # -------------------------

    def create_like(
        self,
        liker_id: str,
        liked_id: str,
    ):

        data = {
            "liker_id": liker_id,
            "liked_id": liked_id,
            "created_at": self._now(),
        }

        response = (
            self.client
            .table("likes")
            .insert(data)
            .execute()
        )

        return response.data[0]

    def has_like(
        self,
        liker_id: str,
        liked_id: str,
    ) -> bool:

        response = (
            self.client
            .table("likes")
            .select("id")
            .eq("liker_id", liker_id)
            .eq("liked_id", liked_id)
            .limit(1)
            .execute()
        )

        return bool(response.data)

    # -------------------------
    # MATCHES
    # -------------------------

    def create_match(
        self,
        user1_id: str,
        user2_id: str,
    ):

        data = {
            "user1_id": user1_id,
            "user2_id": user2_id,
            "created_at": self._now(),
        }

        response = (
            self.client
            .table("matches")
            .insert(data)
            .execute()
        )

        return response.data[0]

    def get_user_matches(
        self,
        user_id: str,
    ):

        response = (
            self.client
            .table("matches")
            .select("*")
            .or_(
                f"user1_id.eq.{user_id},"
                f"user2_id.eq.{user_id}"
            )
            .execute()
        )

        return response.data

    # -------------------------
    # MESSAGES
    # -------------------------

    def create_message(
        self,
        match_id: str,
        sender_id: str,
        content: str,
    ):

        data = {
            "match_id": match_id,
            "sender_id": sender_id,
            "content": content,
            "created_at": self._now(),
        }

        response = (
            self.client
            .table("messages")
            .insert(data)
            .execute()
        )

        return response.data[0]

    def get_messages(
        self,
        match_id: str,
    ):

        response = (
            self.client
            .table("messages")
            .select("*")
            .eq("match_id", match_id)
            .order("created_at")
            .execute()
        )

        return response.data


try:
    repository = SupabaseRepository()
except Exception:
    repository = None