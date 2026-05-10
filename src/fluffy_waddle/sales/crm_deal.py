from decimal import Decimal
from datetime import date, datetime
from pydantic import Field
from .crm_named_model import CRMNamedModel
from .crm_campaign import CRMCampaign
from .crm_contact import CRMContact
from .crm_loss_reason import CRMLossReason
from .crm_organization import CRMOrganization
from .crm_pipeline_stage import CRMPipelineStage
from .crm_product import CRMProduct
from .crm_source import CRMSource
from .crm_task import CRMTask
from .crm_user import CRMUser


class CRMDeal(CRMNamedModel):
    stage: CRMPipelineStage
    owner: CRMUser | None = None
    source: CRMSource | None = None
    campaign: CRMCampaign | None = None
    loss_reason: CRMLossReason | None = None
    organization: CRMOrganization | None = None
    value: Decimal | None = None
    expected_close_date: date | None = None
    rating: int | None = None
    status: str
    closed_at: datetime | None = None
    contacts: list[CRMContact] = Field(default_factory=list)
    products: list[CRMProduct] = Field(default_factory=list)
    tasks: list[CRMTask] = Field(default_factory=list)
