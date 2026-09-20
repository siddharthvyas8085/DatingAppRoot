from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.ai import router as ai_router
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.matches import router as matches_router
from app.api.preferences import router as preferences_router
from app.api.profile import router as profile_router
from app.api.safety import router as safety_router


app = FastAPI(
    title="Dating App API",
    description="Backend API for the dating application",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(preferences_router)
app.include_router(matches_router)
app.include_router(chat_router)
app.include_router(ai_router)
app.include_router(safety_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}