from app.repositories.factory import get_repository


class PreferencesService:
    def create_preferences(self, user_id: str, preferences_data: dict):
        repository = get_repository()
        self._validate_age_range(preferences_data)

        existing = repository.get_preferences(user_id)
        if existing:
            updates = {key: value for key, value in preferences_data.items() if value is not None}
            updated = repository.update_preferences(user_id, updates)
            if updated is None:
                raise ValueError("Preferences not found")
            return updated

        preferences = {
            "user_id": user_id,
            **preferences_data,
            "created_at": repository._now(),
            "updated_at": repository._now(),
        }
        return repository.create_preferences(preferences)

    def get_preferences(self, user_id: str):
        repository = get_repository()
        preferences = repository.get_preferences(user_id)
        if not preferences:
            raise ValueError("Preferences not found")
        return preferences

    def update_preferences(self, user_id: str, preferences_data: dict):
        repository = get_repository()
        existing = repository.get_preferences(user_id)
        if not existing:
            raise ValueError("Preferences not found")

        updates = {key: value for key, value in preferences_data.items() if value is not None}
        merged = {**existing, **updates}
        self._validate_age_range(merged)

        updated = repository.update_preferences(user_id, updates)
        if updated is None:
            raise ValueError("Preferences not found")
        return updated

    def discover_profiles(self, user_id: str):
        repository = get_repository()
        profiles = repository.get_all_profiles()
        preferences = repository.get_preferences(user_id)

        if not preferences:
            return [profile for profile in profiles if profile["id"] != user_id]

        gender = preferences.get("gender")
        min_age = preferences.get("min_age")
        max_age = preferences.get("max_age")
        city = preferences.get("city")

        results = []
        for profile in profiles:
            if profile["id"] == user_id:
                continue
            if gender and profile.get("gender") and profile["gender"].lower() != str(gender).lower():
                continue
            if city and profile.get("city") and profile["city"].lower() != str(city).lower():
                continue
            birth_year = profile.get("date_of_birth")
            if birth_year and (min_age is not None or max_age is not None):
                try:
                    from datetime import date
                    if isinstance(birth_year, str):
                        birth_date = date.fromisoformat(birth_year)
                        age = 2026 - birth_date.year
                        if min_age is not None and age < min_age:
                            continue
                        if max_age is not None and age > max_age:
                            continue
                except Exception:
                    pass
            results.append(profile)

        return results

    def _validate_age_range(self, preferences_data: dict):
        min_age = preferences_data.get("min_age")
        max_age = preferences_data.get("max_age")

        if min_age is not None and max_age is not None and int(min_age) > int(max_age):
            raise ValueError("min_age cannot be greater than max_age")


preferences_service = PreferencesService()
