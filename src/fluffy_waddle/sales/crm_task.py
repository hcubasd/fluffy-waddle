from datetime import datetime
from pydantic import Field
from .crm_named_model import CRMNamedModel
from .crm_user import CRMUser


class CRMTask(CRMNamedModel):
    created_by: CRMUser
    completed_by: CRMUser | None = None
    description: str | None = None
    type: str
    status: str
    due_date: datetime | None = None
    completed_at: datetime | None = None
    assignees: list[CRMUser] = Field(default_factory=list)
