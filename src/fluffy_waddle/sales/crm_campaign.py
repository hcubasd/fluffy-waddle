from typing import Optional
from .crm_named_model import CRMNamedModel


class CRMCampaign(CRMNamedModel):
    description: Optional[str] = None
