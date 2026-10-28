from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    points = Column(Integer, default=0)
    salads_purchased = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    feedbacks = relationship("Feedback", back_populates="user")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    title_name = Column(String(120))
    badge = Column(String(120))
    price = Column(Integer, nullable=False)
    original_price = Column(Integer)
    calories = Column(Integer)
    protein = Column(String(20))
    carbs = Column(String(20))
    fat = Column(String(20))
    fiber = Column(String(20))
    description = Column(Text)
    micronutrients = Column(Text)
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)


class WeeklyMenuItem(Base):
    __tablename__ = "weekly_menu_items"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String(20), nullable=False)  # Monday, Tuesday, etc.
    meal_type = Column(String(20), nullable=False)  # lunch, dinner
    name = Column(String(120), nullable=False)
    title_name = Column(String(120))
    protein = Column(String(20))
    fiber = Column(String(20))
    description = Column(Text)
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)


class TrendingMeal(Base):
    __tablename__ = "trending_meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text)
    badge = Column(String(120))
    image_url = Column(String(500))
    meal_type = Column(String(50))  # e.g. "Lunch favorite"
    is_active = Column(Boolean, default=True)


class TeamProfile(Base):
    __tablename__ = "team_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    role = Column(String(120))
    bio = Column(Text)
    image_url = Column(String(500))
    href = Column(String(500))
    display_order = Column(Integer, default=0)


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(80))
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    content = Column(Text)
    read_time = Column(String(30))
    accent_color = Column(String(20))
    background_color = Column(String(20))
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    is_published = Column(Boolean, default=True)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_name = Column(String(120))
    rating = Column(Integer, nullable=False)           # 1–5
    category = Column(String(80))
    message = Column(Text, nullable=False)
    last_meal = Column(String(120))
    salads_purchased = Column(Integer, default=0)
    points = Column(Integer, default=0)
    approved = Column(Boolean, default=False)          # admin approves before showing publicly
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="feedbacks")
