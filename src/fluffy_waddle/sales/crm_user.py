from typing import Optional
from .crm_named_model import CRMNamedModel

class CRMUser(CRMNamedModel):
    email: Optional[str] = None
    phone: Optional[str] = None
