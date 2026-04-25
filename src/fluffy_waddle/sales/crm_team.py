from pydantic import Field
from .crm_named_model import CRMNamedModel
from .crm_user import CRMUser


class CRMTeam(CRMNamedModel):
    members: list[CRMUser] = Field(default_factory=list)
