from app.repositories.factory import get_repository


class MatchService:
    def like_profile(self, liker_id: str, liked_id: str):
        repository = get_repository()

        if liker_id == liked_id:
            raise ValueError("You cannot like yourself")

        existing_like = repository.has_like(liker_id, liked_id)
        if existing_like:
            return {"matched": False, "message": "Like already exists"}

        repository.create_like(liker_id, liked_id)

        mutual = repository.has_like(liked_id, liker_id)
        if mutual:
            match = repository.create_match(liker_id, liked_id)
            return {"matched": True, "match": match, "message": "It's a match!"}

        return {"matched": False, "message": "Like recorded"}


match_service = MatchService()
