import os

from app.repositories.csv_repository import CSVRepository
from app.repositories.supabase_repository import SupabaseRepository


def get_repository():
    """Return the active repository implementation.

    CSV is the default for local development until Supabase is explicitly
    enabled and the schema matches the application contract.
    """
    use_supabase = os.getenv("USE_SUPABASE", "false").strip().lower()

    if use_supabase not in {"1", "true", "yes", "on"}:
        return CSVRepository()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not (supabase_url and supabase_key):
        return CSVRepository()

    try:
        return SupabaseRepository()
    except Exception:
        return CSVRepository()
