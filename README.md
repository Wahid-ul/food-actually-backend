# Food, Actually — Backend

FastAPI + PostgreSQL + JWT authentication.

## Setup

### 1. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Create PostgreSQL database

```bash
psql -U postgres
CREATE DATABASE food_actually;
\q
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your DB credentials and secret key
```

### 4. Run migrations (creates all tables)

```bash
alembic upgrade head
```

Or let FastAPI auto-create on startup (dev only):
```python
# main.py already has: Base.metadata.create_all(bind=engine)
```

### 5. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

API will run at `http://localhost:8000`

Docs at `http://localhost:8000/docs`

---

## API Endpoints

### Auth
- `POST /auth/register` — { name, email, password }
- `POST /auth/login` — { email, password } → returns JWT
- `GET /auth/me` — get current user (requires Bearer token)

### Menu
- `GET /menu/items` — all active menu items
- `GET /menu/trending` — trending meals

### Feedback
- `POST /feedback/` — submit feedback (auth optional)
- `GET /feedback/approved` — public approved reviews

### Blog
- `GET /blog/posts` — all published posts
- `GET /blog/posts/{id}` — single post

### Team
- `GET /team/` — team profiles

---

## Database Migrations with Alembic

Create a new migration after model changes:
```bash
alembic revision --autogenerate -m "your message"
alembic upgrade head
```

---

## Production Deployment

1. Set environment variables on your host (Railway, Render, etc.)
2. Use a managed Postgres instance
3. Set `SECRET_KEY` to a strong random value
4. Update `allow_origins` in `main.py` CORS to your production domain
