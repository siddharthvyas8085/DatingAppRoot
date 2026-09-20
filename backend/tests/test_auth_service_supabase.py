from app.services import auth_service as auth_service_module


def test_register_uses_supabase_auth_when_enabled(monkeypatch):
    monkeypatch.setattr(
        auth_service_module,
        "is_supabase_auth_enabled",
        lambda: True,
    )

    captured = {}

    def fake_sign_up(email, password):
        captured["email"] = email
        captured["password"] = password
        return {"id": "supabase-user-1", "email": email}

    monkeypatch.setattr(
        auth_service_module,
        "sign_up_with_supabase",
        fake_sign_up,
    )

    result = auth_service_module.AuthService().register_user(
        "user@example.com",
        "StrongPass123!",
    )

    assert result == {"id": "supabase-user-1", "email": "user@example.com"}
    assert captured == {"email": "user@example.com", "password": "StrongPass123!"}


def test_login_uses_supabase_auth_when_enabled(monkeypatch):
    monkeypatch.setattr(
        auth_service_module,
        "is_supabase_auth_enabled",
        lambda: True,
    )

    captured = {}

    def fake_sign_in(email, password):
        captured["email"] = email
        captured["password"] = password
        return {
            "id": "supabase-user-2",
            "email": email,
            "access_token": "supabase-token-xyz",
        }

    monkeypatch.setattr(
        auth_service_module,
        "sign_in_with_supabase",
        fake_sign_in,
    )

    result = auth_service_module.AuthService().login_user(
        "user@example.com",
        "StrongPass123!",
    )

    assert result == {
        "id": "supabase-user-2",
        "email": "user@example.com",
        "access_token": "supabase-token-xyz",
    }
    assert captured == {"email": "user@example.com", "password": "StrongPass123!"}
