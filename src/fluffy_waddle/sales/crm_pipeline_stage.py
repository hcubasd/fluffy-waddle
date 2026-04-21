from typing import Optional
from .crm_named_model import CRMNamedModel
from .crm_pipeline import CRMPipeline


class CRMPipelineStage(CRMNamedModel):
    pipeline: CRMPipeline
    description: Optional[str] = None
    objective: Optional[str] = None
    display_order: int
