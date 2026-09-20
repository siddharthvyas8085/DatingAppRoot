from datetime import date

from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    date_of_birth: date | None = None
    gender: str | None = None
    bio: str | None = Field(default=None, max_length=500)
    occupation: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    profile_image_url: str | None = None


class ProfileResponse(BaseModel):
    id: str
    name: str
    date_of_birth: date | None = None
    gender: str | None = None
    bio: str | None = None
    occupation: str | None = None
    city: str | None = None
    profile_image_url: str | None = None
    created_at: str
    updated_at: str


class ProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    date_of_birth: date | None = None
    gender: str | None = None
    bio: str | None = Field(default=None, max_length=500)
    occupation: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    profile_image_url: str | None = None