from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import BlogPost
from ..schemas import BlogPostOut

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get("/posts", response_model=List[BlogPostOut])
def get_posts(db: Session = Depends(get_db)):
    return (
        db.query(BlogPost)
        .filter(BlogPost.is_published == True)
        .order_by(BlogPost.published_at.desc())
        .all()
    )


@router.get("/posts/{post_id}", response_model=BlogPostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id, BlogPost.is_published == True).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return post
