from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from api.database import get_db
from api.schemas import MessageResult
from api.crud.analytics import search_messages

router = APIRouter()


# ---------- Endpoint 3: Message Search ----------
@router.get("/messages", response_model=List[MessageResult])
def search_messages_endpoint(
    query: str = Query(..., description="Keyword to search in messages"),
    limit: int = Query(20, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Search messages containing a specific keyword across all channels.
    """
    return search_messages(db=db, query=query, limit=limit)
