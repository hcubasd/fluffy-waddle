from .crm_model import CRMModel
from .crm_team import CRMTeam


class CRMUser(CRMModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    team: CRMTeam | None = None
