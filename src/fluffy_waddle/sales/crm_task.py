from datetime import datetime
from typing import Optional
from .crm_named_model import CRMNamedModel
from .crm_user import CRMUser


class CRMTask(CRMNamedModel):
    created_by: CRMUser
    completed_by: Optional[CRMUser] = None
    deal_id: Optional[str] = None
    description: Optional[str] = None
    type: str
    status: str
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    owners: list[CRMUser] = []
