from typing import Any
from pydantic import Field
from .crm_named_model import CRMNamedModel
from .crm_organization import CRMOrganization


class CRMContact(CRMNamedModel):
    organization: CRMOrganization | None = None
    job_title: str | None = None
    emails: list[dict[str, Any]] = Field(default_factory=list)
    phones: list[dict[str, Any]] = Field(default_factory=list)
    social_profiles: list[dict[str, Any]] = Field(default_factory=list)
    legal_bases: list[dict[str, Any]] = Field(default_factory=list)
