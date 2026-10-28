from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .database import engine, Base
from .routers import auth, menu, feedback, blog, team, weekly_menu, booking

load_dotenv()

# Create all tables on startup (use Alembic for production migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food, Actually API",
    description="Backend for Food, Actually — menu, auth, feedback, blog, team.",
    version="1.0.0",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
# Allow the React dev server and production domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",
        "https://food-actually.vercel.app",  # update to your prod domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(feedback.router)
app.include_router(blog.router)
app.include_router(team.router)
app.include_router(weekly_menu.router)
app.include_router(booking.router)


@app.get("/")
def root():
    return {"status": "Food, Actually API is running."}


@app.get("/health")
def health():
    return {"status": "ok"}
