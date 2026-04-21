from typing import Optional
from .crm_named_model import CRMNamedModel


class CRMContact(CRMNamedModel):
    organization_id: Optional[str] = None
    job_title: Optional[str] = None
    emails: list = []
    phones: list = []
    social_profiles: list = []
    legal_bases: list = []
