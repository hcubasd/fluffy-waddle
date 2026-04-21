from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .crm_user import CRMUser


class CRMDealNote(BaseModel):
    id: str
    deal_id: str
    author: CRMUser
    description: str
    created_at: datetime
    pinned_at: Optional[datetime] = None
    edited_by: Optional[CRMUser] = None
    edited_at: Optional[datetime] = None
