from app.repositories.factory import get_repository

repository = get_repository()


class ProfileService:

    def create_profile(
        self,
        user_id: str,
        profile_data: dict,
    ):

        existing_profile = repository.get_profile(user_id)

        if existing_profile:
            raise ValueError(
                "Profile already exists"
            )

        profile = {
            "id": user_id,
            **profile_data,
            "created_at": repository._now(),
            "updated_at": repository._now(),
        }

        return repository.create_profile(profile)

    def get_profile(self, user_id: str):

        profile = repository.get_profile(user_id)

        if not profile:
            raise ValueError(
                "Profile not found"
            )

        return profile

    def update_profile(
        self,
        user_id: str,
        profile_data: dict,
    ):

        existing_profile = repository.get_profile(user_id)

        if not existing_profile:
            raise ValueError(
                "Profile not found"
            )

        # Only update fields actually supplied
        updates = {
            key: value
            for key, value in profile_data.items()
            if value is not None
        }

        return repository.update_profile(
            user_id,
            updates,
        )


profile_service = ProfileService()