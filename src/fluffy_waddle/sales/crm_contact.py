from typing import Optional
from .crm_named_model import CRMNamedModel
from .crm_organization import CRMOrganization


class CRMContact(CRMNamedModel):
    organization: Optional[CRMOrganization] = None
    job_title: Optional[str] = None
    emails: list = []
    phones: list = []
    social_profiles: list = []
    legal_bases: list = []
