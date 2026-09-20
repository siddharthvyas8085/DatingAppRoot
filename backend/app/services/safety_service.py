from app.repositories.factory import get_repository


class SafetyService:
    def block_user(self, blocker_id: str, blocked_id: str):
        repository = get_repository()
        if blocker_id == blocked_id:
            raise ValueError("You cannot block yourself")

        record = {
            "id": __import__("uuid").uuid4().__str__(),
            "blocker_id": blocker_id,
            "blocked_id": blocked_id,
            "created_at": repository._now(),
        }
        repository._append("blocks.csv", record)
        return record

    def report_user(self, reporter_id: str, reported_id: str, reason: str):
        repository = get_repository()
        if not reason or not reason.strip():
            raise ValueError("Reason is required")

        record = {
            "id": __import__("uuid").uuid4().__str__(),
            "reporter_id": reporter_id,
            "reported_id": reported_id,
            "reason": reason.strip(),
            "created_at": repository._now(),
        }
        repository._append("reports.csv", record)
        return record

    def unmatch_users(self, user1_id: str, user2_id: str):
        repository = get_repository()
        matches = repository._read("matches.csv")
        filtered = [
            match for match in matches
            if not (
                (match.get("user1_id") == user1_id and match.get("user2_id") == user2_id)
                or (match.get("user1_id") == user2_id and match.get("user2_id") == user1_id)
            )
        ]

        if len(filtered) == len(matches):
            return {"status": "not_found"}

        repository._write("matches.csv", filtered)
        return {"status": "unmatched", "user1_id": user1_id, "user2_id": user2_id}


safety_service = SafetyService()
