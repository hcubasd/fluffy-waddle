from datetime import datetime
from pydantic import BaseModel
from .crm_user import CRMUser

class CRMDealNote(BaseModel):
    id: str
    author: CRMUser
    description: str
    created_at: datetime
    pinned_at: datetime | None = None
    edited_by: CRMUser | None = None
    edited_at: datetime | None = None
