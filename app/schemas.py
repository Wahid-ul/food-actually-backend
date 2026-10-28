from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── Auth ────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    points: int
    salads_purchased: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


# ── Menu ─────────────────────────────────────────────────────────────────────

class MenuItemCreate(BaseModel):
    name: str
    title_name: Optional[str] = None
    badge: Optional[str] = None
    price: int
    original_price: Optional[int] = None
    calories: Optional[int] = None
    protein: Optional[str] = None
    carbs: Optional[str] = None
    fat: Optional[str] = None
    fiber: Optional[str] = None
    description: Optional[str] = None
    micronutrients: Optional[str] = None
    image_url: str


class MenuItemOut(BaseModel):
    id: int
    name: str
    title_name: Optional[str]
    badge: Optional[str]
    price: int
    original_price: Optional[int]
    calories: Optional[int]
    protein: Optional[str]
    carbs: Optional[str]
    fat: Optional[str]
    fiber: Optional[str]
    description: Optional[str]
    micronutrients: Optional[str]
    image_url: Optional[str]

    class Config:
        from_attributes = True


# ── Weekly Menu ──────────────────────────────────────────────────────────────

class WeeklyMenuItemCreate(BaseModel):
    day_of_week: str
    meal_type: str
    name: str
    title_name: Optional[str] = None
    protein: Optional[str] = None
    fiber: Optional[str] = None
    description: Optional[str] = None
    image_url: str


class WeeklyMenuItemOut(BaseModel):
    id: int
    day_of_week: str
    meal_type: str
    name: str
    title_name: Optional[str]
    protein: Optional[str]
    fiber: Optional[str]
    description: Optional[str]
    image_url: Optional[str]

    class Config:
        from_attributes = True


# ── Trending ──────────────────────────────────────────────────────────────────

class TrendingMealOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    badge: Optional[str]
    image_url: Optional[str]
    meal_type: Optional[str]

    class Config:
        from_attributes = True


# ── Team ──────────────────────────────────────────────────────────────────────

class TeamProfileOut(BaseModel):
    id: int
    name: str
    role: Optional[str]
    bio: Optional[str]
    image_url: Optional[str]
    href: Optional[str]

    class Config:
        from_attributes = True


# ── Blog ──────────────────────────────────────────────────────────────────────

class BlogPostOut(BaseModel):
    id: int
    tag: Optional[str]
    title: str
    summary: Optional[str]
    content: Optional[str]
    read_time: Optional[str]
    accent_color: Optional[str]
    background_color: Optional[str]
    published_at: datetime

    class Config:
        from_attributes = True


# ── Feedback ──────────────────────────────────────────────────────────────────

class FeedbackCreate(BaseModel):
    rating: int
    category: str
    message: str
    last_meal: Optional[str] = None
    salads_purchased: Optional[int] = 0
    points: Optional[int] = 0


class FeedbackOut(BaseModel):
    id: int
    user_name: Optional[str]
    rating: int
    category: str
    message: str
    last_meal: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Booking ───────────────────────────────────────────────────────────────────

class BookingCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    meal_name: str
    meal_type: Optional[str] = None
    delivery_date: str
    delivery_slot: str
    preferred_location: str
    special_requests: Optional[str] = None
