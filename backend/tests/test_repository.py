from app.repositories.csv_repository import CSVRepository
from app.repositories.factory import get_repository


def test_create_user():

    repository = CSVRepository()

    user = repository.create_user(
        email="test@example.com",
        password_hash="hashed-password"
    )

    assert user["email"] == "test@example.com"

    saved_user = repository.get_user_by_id(user["id"])

    assert saved_user is not None
    assert saved_user["email"] == "test@example.com"


def test_repository_factory_falls_back_to_csv_when_supabase_not_configured(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)

    repository = get_repository()

    assert isinstance(repository, CSVRepository)


def test_repository_factory_falls_back_to_csv_when_supabase_is_incompatible(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test-key")

    original = __import__("app.repositories.factory", fromlist=["SupabaseRepository"]).__dict__.get("SupabaseRepository")

    def fake_supabase_repository():
        raise RuntimeError("public.users table not found")

    import app.repositories.factory as factory_module
    factory_module.SupabaseRepository = fake_supabase_repository

    try:
        repository = get_repository()
        assert isinstance(repository, CSVRepository)
    finally:
        if original is not None:
            factory_module.SupabaseRepository = original
