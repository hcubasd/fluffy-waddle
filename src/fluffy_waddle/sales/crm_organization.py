from typing import Optional
from .crm_named_model import CRMNamedModel
from .crm_segment import CRMSegment
from .crm_user import CRMUser


class CRMOrganization(CRMNamedModel):
    owner_id: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    address: Optional[dict] = None
    segments: list[CRMSegment] = []
    followers: list[CRMUser] = []
