from pydantic import Field
from .crm_named_model import CRMNamedModel


class CRMContact(CRMNamedModel):
    job_title: str | None = None
    emails: list[dict] = Field(default_factory=list)
    phones: list[dict] = Field(default_factory=list)
    social_profiles: list[dict] = Field(default_factory=list)
