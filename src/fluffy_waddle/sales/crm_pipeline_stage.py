from .crm_named_model import CRMNamedModel
from .crm_pipeline import CRMPipeline


class CRMPipelineStage(CRMNamedModel):
    pipeline: CRMPipeline
    description: str | None = None
    objective: str | None = None
    display_order: int
