from pydantic import BaseModel, Field


class PreferencesCreate(BaseModel):
    gender: str | None = None
    min_age: int | None = Field(default=None, ge=18, le=80)
    max_age: int | None = Field(default=None, ge=18, le=80)
    city: str | None = Field(default=None, max_length=100)
    distance_km: int | None = Field(default=None, ge=1, le=500)


class PreferencesResponse(BaseModel):
    user_id: str
    gender: str | None = None
    min_age: int | None = None
    max_age: int | None = None
    city: str | None = None
    distance_km: int | None = None
    created_at: str | None = None
    updated_at: str | None = None


class PreferencesUpdate(BaseModel):
    gender: str | None = None
    min_age: int | None = Field(default=None, ge=18, le=80)
    max_age: int | None = Field(default=None, ge=18, le=80)
    city: str | None = Field(default=None, max_length=100)
    distance_km: int | None = Field(default=None, ge=1, le=500)
