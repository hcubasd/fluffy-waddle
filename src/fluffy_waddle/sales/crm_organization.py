from typing import Any
from pydantic import Field
from .crm_named_model import CRMNamedModel
from .crm_industry import CRMIndustry
from .crm_user import CRMUser


class CRMOrganization(CRMNamedModel):
    owner: CRMUser | None = None
    description: str | None = None
    url: str | None = None
    address: dict[str, Any] | None = None
    industries: list[CRMIndustry] = Field(default_factory=list)
    followers: list[CRMUser] = Field(default_factory=list)
