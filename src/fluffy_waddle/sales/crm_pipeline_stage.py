from typing import Optional
from .crm_named_model import CRMNamedModel


class CRMPipelineStage(CRMNamedModel):
    pipeline_id: str
    description: Optional[str] = None
    objective: Optional[str] = None
    display_order: int
