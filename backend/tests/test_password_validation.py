import pytest
from pydantic import ValidationError

from app.schemas.auth import RegisterRequest


def test_register_request_rejects_password_longer_than_72_bytes():
    long_password = "a" * 73

    with pytest.raises(ValidationError, match="Password must be 72 bytes or fewer"):
        RegisterRequest(email="test@example.com", password=long_password)
