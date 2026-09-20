import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext


load_dotenv()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-secret-key",
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
        "60",
    )
)


def hash_password(password: str) -> str:
    normalized = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(normalized)


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:

    return pwd_context.verify(
        plain_password,
        password_hash,
    )


def create_access_token(user_id: str) -> str:

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )