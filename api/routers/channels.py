from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.database import get_db
from api.schemas import ChannelActivity
from api.crud.analytics import get_channel_activity

router = APIRouter()


# ---------- Endpoint 2: Channel Activity ----------
@router.get("/{channel_name}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    """
    Returns posting activity and trends for a specific channel.
    """
    return get_channel_activity(db=db, channel_name=channel_name)
