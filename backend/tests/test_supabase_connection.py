import os

import pytest
from dotenv import load_dotenv
from supabase import create_client


load_dotenv()


def test_supabase_connection():
    if os.getenv("USE_SUPABASE", "false").lower() not in {"1", "true", "yes", "on"}:
        pytest.skip("Supabase is disabled for local CSV mode")

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    assert supabase_url, "SUPABASE_URL is missing"
    assert supabase_key, "SUPABASE_KEY is missing"

    supabase = create_client(
        supabase_url,
        supabase_key,
    )

    response = (
        supabase
        .table("profiles")
        .select("id")
        .limit(1)
        .execute()
    )

    assert response is not None