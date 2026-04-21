from typing import Optional
from .crm_named_model import CRMNamedModel


class CRMSource(CRMNamedModel):
    description: Optional[str] = None
