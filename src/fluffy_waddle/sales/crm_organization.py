from pydantic import Field
from .crm_named_model import CRMNamedModel
from .crm_industry import CRMIndustry
from .crm_user import CRMUser
from .crm_contact import CRMContact

class CRMOrganization(CRMNamedModel):
    owner: CRMUser | None = None
    description: str | None = None
    url: str | None = None
    address: dict | None = None
    industries: list[CRMIndustry] = Field(default_factory=list)
    followers: list[CRMUser] = Field(default_factory=list)
    contacts: list[CRMContact] = Field(default_factory=list)
