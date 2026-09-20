from app.repositories.factory import get_repository


class ChatService:
    def send_message(self, match_id: str, sender_id: str, content: str):
        repository = get_repository()
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")

        self._require_match_member(repository, match_id, sender_id)
        return repository.create_message(match_id, sender_id, content.strip())

    def get_messages_for_match(self, match_id: str, user_id: str):
        repository = get_repository()
        self._require_match_member(repository, match_id, user_id)
        messages = repository.get_messages(match_id)
        return [message for message in messages if message.get("match_id") == match_id]

    def _require_match_member(self, repository, match_id: str, user_id: str):
        matches = repository.get_user_matches(user_id)

        for match in matches:
            if match.get("id") == match_id:
                return

        raise ValueError("User is not a member of this match")


chat_service = ChatService()
