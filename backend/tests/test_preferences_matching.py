from pathlib import Path

from app.repositories.csv_repository import CSVRepository
from app.services.match_service import match_service
from app.services.preferences_service import preferences_service

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def clear_csv_state():
    for filename in [
        "users.csv",
        "profiles.csv",
        "preferences.csv",
        "likes.csv",
        "matches.csv",
        "messages.csv",
        "blocks.csv",
        "reports.csv",
    ]:
        path = DATA_DIR / filename
        if path.exists():
            path.unlink()


def test_preferences_round_trip():
    clear_csv_state()
    repo = CSVRepository()
    user_id = "user-preferences-1"

    repo.create_profile({
        "id": user_id,
        "name": "Alice",
        "gender": "female",
        "date_of_birth": "1995-01-01",
        "bio": "Looking for a serious relationship",
        "occupation": "Designer",
        "city": "Delhi",
        "profile_image_url": "",
        "created_at": repo._now(),
        "updated_at": repo._now(),
    })

    created = preferences_service.create_preferences(user_id, {
        "gender": "male",
        "min_age": 25,
        "max_age": 40,
        "city": "Delhi",
        "distance_km": 50,
    })

    assert created["user_id"] == user_id
    assert preferences_service.get_preferences(user_id)["city"] == "Delhi"

    updated = preferences_service.update_preferences(user_id, {
        "city": "Mumbai",
        "min_age": 26,
    })

    assert updated["city"] == "Mumbai"
    assert int(preferences_service.get_preferences(user_id)["min_age"]) == 26
    assert preferences_service.get_preferences(user_id)["city"] == "Mumbai"


def test_preferences_reject_invalid_age_range():
    clear_csv_state()

    try:
        preferences_service.create_preferences("user-invalid-age", {
            "min_age": 45,
            "max_age": 30,
        })
    except ValueError as error:
        assert str(error) == "min_age cannot be greater than max_age"
    else:
        raise AssertionError("Expected invalid age range to be rejected")


def test_discovery_excludes_self_and_respects_preferences():
    clear_csv_state()
    repo = CSVRepository()
    user_id = "user-discovery-1"
    other_user = "user-discovery-2"

    repo.create_profile({
        "id": user_id,
        "name": "Alice",
        "gender": "female",
        "date_of_birth": "1996-01-01",
        "bio": "Introvert",
        "occupation": "Product",
        "city": "Delhi",
        "profile_image_url": "",
        "created_at": repo._now(),
        "updated_at": repo._now(),
    })

    repo.create_profile({
        "id": other_user,
        "name": "Bob",
        "gender": "male",
        "date_of_birth": "1990-01-01",
        "bio": "Outdoorsy",
        "occupation": "Engineer",
        "city": "Delhi",
        "profile_image_url": "",
        "created_at": repo._now(),
        "updated_at": repo._now(),
    })

    preferences_service.create_preferences(user_id, {
        "gender": "male",
        "min_age": 25,
        "max_age": 35,
        "city": "Delhi",
        "distance_km": 100,
    })

    discovered = preferences_service.discover_profiles(user_id)
    assert any(profile["id"] == other_user for profile in discovered)
    assert all(profile["id"] != user_id for profile in discovered)


def test_like_flow_creates_match_when_mutual_like_happens():
    clear_csv_state()
    repo = CSVRepository()
    user_a = "like-user-a"
    user_b = "like-user-b"

    for profile_id, name in [(user_a, "A"), (user_b, "B")]:
        repo.create_profile({
            "id": profile_id,
            "name": name,
            "gender": "female" if profile_id == user_a else "male",
            "date_of_birth": "1994-01-01",
            "bio": "Test user",
            "occupation": "Engineer",
            "city": "Delhi",
            "profile_image_url": "",
            "created_at": repo._now(),
            "updated_at": repo._now(),
        })

    first_like = match_service.like_profile(user_a, user_b)
    assert first_like["matched"] is False

    second_like = match_service.like_profile(user_b, user_a)
    assert second_like["matched"] is True
    assert second_like["match"]["user1_id"] in {user_a, user_b}
    assert second_like["match"]["user2_id"] in {user_a, user_b}
