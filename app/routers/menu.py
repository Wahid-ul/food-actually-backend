from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

from ..database import get_db
from ..models import MenuItem, TrendingMeal
from ..schemas import MenuItemOut, TrendingMealOut, MenuItemCreate

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("/items", response_model=List[MenuItemOut])
def get_menu_items(db: Session = Depends(get_db)):
    return db.query(MenuItem).filter(MenuItem.is_active == True).all()


@router.get("/items/{item_id}", response_model=MenuItemOut)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    menu_item = db.query(MenuItem).filter(MenuItem.id == item_id, MenuItem.is_active == True).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item


@router.get("/trending", response_model=List[TrendingMealOut])
def get_trending_meals(db: Session = Depends(get_db)):
    return db.query(TrendingMeal).filter(TrendingMeal.is_active == True).all()


@router.post("/upload_image")
def upload_image(file: UploadFile = File(...)):
    try:
        upload_result = cloudinary.uploader.upload(
            file.file,
            folder="menu_items",
            resource_type="image"
        )
        return {"url": upload_result["secure_url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin_upload", response_model=MenuItemOut)
def create_menu_item(menu_item: MenuItemCreate, db: Session = Depends(get_db)):
    # Create new menu item with the provided Cloudinary URL
    db_menu_item = MenuItem(
        name=menu_item.name,
        title_name=menu_item.title_name,
        badge=menu_item.badge,
        price=menu_item.price,
        original_price=menu_item.original_price,
        calories=menu_item.calories,
        protein=menu_item.protein,
        carbs=menu_item.carbs,
        fat=menu_item.fat,
        fiber=menu_item.fiber,
        description=menu_item.description,
        micronutrients=menu_item.micronutrients,
        image_url=menu_item.image_url,
        is_active=True
    )

    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)

    return db_menu_item
