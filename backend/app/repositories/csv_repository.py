import csv
import uuid
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


class CSVRepository:

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, filename: str) -> Path:
        return self.data_dir / filename

    def _read(self, filename: str):
        file_path = self._file_path(filename)

        if not file_path.exists():
            return []

        with open(
            file_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            return list(csv.DictReader(file))

    def _write(self, filename: str, rows: list[dict]):
        file_path = self._file_path(filename)

        if not rows:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                file.write("")
            return

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=rows[0].keys()
            )

            writer.writeheader()
            writer.writerows(rows)

    def _append(self, filename: str, row: dict):
        file_path = self._file_path(filename)

        file_exists = file_path.exists()
        file_has_data = (
            file_exists
            and file_path.stat().st_size > 0
        )

        with open(
            file_path,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=row.keys()
            )

            # Create header only if the file is empty.
            if not file_has_data:
                writer.writeheader()

            writer.writerow(row)

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    # ============================================
    # USERS
    # ============================================

    def create_user(
        self,
        email: str,
        password_hash: str
    ):

        user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password_hash": password_hash,
            "created_at": self._now(),
        }
        file_path = self._file_path("users.csv")
        # Ensure users.csv exists with the correct headers
        if not file_path.exists() or file_path.stat().st_size == 0:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["id", "email", "password_hash", "created_at"]
                )
                writer.writeheader()

        self._append("users.csv", user)

        return user

    def get_user_by_email(self, email: str):

        users = self._read("users.csv")

        for user in users:
            if user["email"].lower() == email.lower():
                return user

        return None

    def get_user_by_id(self, user_id: str):

        users = self._read("users.csv")

        for user in users:
            if user["id"] == user_id:
                return user

        return None

    # ============================================
    # PROFILES
    # ============================================

    def create_profile(self, profile: dict):
        self._append("profiles.csv", profile)

        return profile

    def get_profile(self, user_id: str):

        profiles = self._read("profiles.csv")

        for profile in profiles:
            if profile["id"] == user_id:
                return profile

        return None

    def get_all_profiles(self):

        return self._read("profiles.csv")

    def update_profile(
        self,
        user_id: str,
        updates: dict
    ):

        profiles = self._read("profiles.csv")

        for profile in profiles:

            if profile["id"] == user_id:

                profile.update(updates)
                profile["updated_at"] = self._now()

        self._write("profiles.csv", profiles)

        return self.get_profile(user_id)

    # ============================================
    # PREFERENCES
    # ============================================

    def create_preferences(
        self,
        preferences: dict
    ):

        self._append(
            "preferences.csv",
            preferences
        )

        return preferences

    def update_preferences(
        self,
        user_id: str,
        updates: dict
    ):

        preferences = self._read("preferences.csv")

        for preference in preferences:

            if preference["user_id"] == user_id:

                preference.update(updates)
                preference["updated_at"] = self._now()
                self._write("preferences.csv", preferences)
                return preference

        return None

    def get_preferences(self, user_id: str):

        preferences = self._read(
            "preferences.csv"
        )

        for preference in preferences:

            if preference["user_id"] == user_id:
                return preference

        return None

    # ============================================
    # LIKES
    # ============================================

    def create_like(
        self,
        liker_id: str,
        liked_id: str
    ):

        likes = self._read("likes.csv")

        for like in likes:

            if (
                like["liker_id"] == liker_id
                and like["liked_id"] == liked_id
            ):
                return like

        like = {
            "id": str(uuid.uuid4()),
            "liker_id": liker_id,
            "liked_id": liked_id,
            "created_at": self._now(),
        }
        file_path = self._file_path("likes.csv")
        # Ensure likes.csv exists with the correct headers
        if not file_path.exists() or file_path.stat().st_size == 0:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["id", "liker_id", "liked_id", "created_at"]
                )
                writer.writeheader()
        self._append("likes.csv", like)

        return like

    def has_like(
        self,
        liker_id: str,
        liked_id: str
    ):

        likes = self._read("likes.csv")

        return any(
            like["liker_id"] == liker_id
            and like["liked_id"] == liked_id
            for like in likes
        )

    # ============================================
    # MATCHES
    # ============================================

    def create_match(
        self,
        user1_id: str,
        user2_id: str
    ):

        matches = self._read("matches.csv")

        for match in matches:

            if (
                {
                    match["user1_id"],
                    match["user2_id"]
                }
                ==
                {
                    user1_id,
                    user2_id
                }
            ):
                return match

        match = {
            "id": str(uuid.uuid4()),
            "user1_id": user1_id,
            "user2_id": user2_id,
            "created_at": self._now(),
        }
        file_path = self._file_path("matches.csv")
        # Ensure matches.csv exists with the correct headers
        if not file_path.exists() or file_path.stat().st_size == 0:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                            fieldnames=["id", "user1_id", "user2_id", "created_at"]
                        )
                writer.writeheader()
        self._append("matches.csv", match)

        return match

    def get_user_matches(self, user_id: str):

        matches = self._read("matches.csv")

        return [
            match
            for match in matches
            if (
                match["user1_id"] == user_id
                or match["user2_id"] == user_id
            )
        ]

    # ============================================
    # MESSAGES
    # ============================================

    def create_message(
        self,
        match_id: str,
        sender_id: str,
        content: str
    ):

        message = {
            "id": str(uuid.uuid4()),
            "match_id": match_id,
            "sender_id": sender_id,
            "content": content,
            "created_at": self._now(),
        }

        file_path = self._file_path("messages.csv")
        # Ensure messages.csv exists with the correct headers
        if not file_path.exists() or file_path.stat().st_size == 0:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["id", "match_id", "sender_id", "content", "created_at"]
                )
                writer.writeheader()
        self._append(
            "messages.csv",
            message
        )

        return message

    def get_messages(self, match_id: str):

        messages = self._read("messages.csv")

        return [
            message
            for message in messages
            if message["match_id"] == match_id
        ]


repository = CSVRepository()
