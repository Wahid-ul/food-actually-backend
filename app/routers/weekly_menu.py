from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

from ..database import get_db
from ..models import WeeklyMenuItem
from ..schemas import WeeklyMenuItemOut, WeeklyMenuItemCreate

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

router = APIRouter(prefix="/weekly-menu", tags=["Weekly Menu"])


@router.get("/items", response_model=List[WeeklyMenuItemOut])
def get_weekly_menu_items(db: Session = Depends(get_db)):
    return db.query(WeeklyMenuItem).filter(WeeklyMenuItem.is_active == True).all()


@router.get("/items/{item_id}", response_model=WeeklyMenuItemOut)
def get_weekly_menu_item(item_id: int, db: Session = Depends(get_db)):
    weekly_item = db.query(WeeklyMenuItem).filter(WeeklyMenuItem.id == item_id, WeeklyMenuItem.is_active == True).first()
    if not weekly_item:
        raise HTTPException(status_code=404, detail="Weekly menu item not found")
    return weekly_item


@router.post("/upload_image")
def upload_image(file: UploadFile = File(...)):
    try:
        upload_result = cloudinary.uploader.upload(
            file.file,
            folder="weekly_menu",
            resource_type="image"
        )
        return {"url": upload_result["secure_url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin_upload", response_model=WeeklyMenuItemOut)
def create_weekly_menu_item(menu_item: WeeklyMenuItemCreate, db: Session = Depends(get_db)):
    # Create new weekly menu item with the provided Cloudinary URL
    db_weekly_item = WeeklyMenuItem(
        day_of_week=menu_item.day_of_week,
        meal_type=menu_item.meal_type,
        name=menu_item.name,
        title_name=menu_item.title_name,
        protein=menu_item.protein,
        fiber=menu_item.fiber,
        description=menu_item.description,
        image_url=menu_item.image_url,
        is_active=True
    )

    db.add(db_weekly_item)
    db.commit()
    db.refresh(db_weekly_item)

    return db_weekly_item
