from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from .crm_named_model import CRMNamedModel
from .crm_pipeline_stage import CRMPipelineStage
from .crm_user import CRMUser
from .crm_source import CRMSource
from .crm_campaign import CRMCampaign
from .crm_lost_reason import CRMLostReason
from .crm_organization import CRMOrganization
from .crm_contact import CRMContact
from .crm_deal_product import CRMDealProduct
from .crm_deal_note import CRMDealNote
from .crm_task import CRMTask


class CRMDeal(CRMNamedModel):
    stage: CRMPipelineStage
    owner: Optional[CRMUser] = None
    source: Optional[CRMSource] = None
    campaign: Optional[CRMCampaign] = None
    lost_reason: Optional[CRMLostReason] = None
    organization: Optional[CRMOrganization] = None
    recurrence_price: Decimal = Decimal("0")
    one_time_price: Decimal = Decimal("0")
    total_price: Decimal = Decimal("0")
    expected_close_date: Optional[date] = None
    rating: Optional[int] = None
    status: str
    closed_at: Optional[datetime] = None
    distribution_settings: Optional[dict] = None
    contacts: list[CRMContact] = []
    products: list[CRMDealProduct] = []
    notes: list[CRMDealNote] = []
    tasks: list[CRMTask] = []
