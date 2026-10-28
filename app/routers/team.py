from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import TeamProfile
from ..schemas import TeamProfileOut

router = APIRouter(prefix="/team", tags=["Team"])


@router.get("/", response_model=List[TeamProfileOut])
def get_team(db: Session = Depends(get_db)):
    return db.query(TeamProfile).order_by(TeamProfile.display_order).all()
