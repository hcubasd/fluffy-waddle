from pydantic import Field
from .crm_model import CRMModel


class CRMContact(CRMModel):
    full_name: str
    job_title: str | None = None
    emails: list[dict] = Field(default_factory=list)
    phones: list[dict] = Field(default_factory=list)
    social_profiles: list[dict] = Field(default_factory=list)
