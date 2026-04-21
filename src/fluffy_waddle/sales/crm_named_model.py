from .crm_model import CRMModel
from typing import Optional

class CRMNamedModel(CRMModel):
    name: Optional[str] = None
