from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from api.database import get_db
from api.schemas import TopProduct, VisualContentStat
from api.crud.analytics import get_top_products, get_visual_content_stats

router = APIRouter()


# ---------- Endpoint 1: Top Products ----------
@router.get("/top-products", response_model=List[TopProduct])
def top_products(limit: int = Query(10, description="Number of top products to return"),
                 db: Session = Depends(get_db)):
    """
    Returns the most frequently mentioned products/terms across all channels.
    """
    return get_top_products(db=db, limit=limit)


# ---------- Endpoint 4: Visual Content Stats ----------
@router.get("/visual-content", response_model=List[VisualContentStat])
def visual_content_stats(db: Session = Depends(get_db)):
    """
    Returns statistics about image usage across channels by category.
    """
    return get_visual_content_stats(db=db)
