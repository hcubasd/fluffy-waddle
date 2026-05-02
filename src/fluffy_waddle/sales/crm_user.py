from .crm_named_model import CRMNamedModel
from .crm_team import CRMTeam


class CRMUser(CRMNamedModel):
    email: str | None = None
    phone: str | None = None
    team: CRMTeam | None = None
