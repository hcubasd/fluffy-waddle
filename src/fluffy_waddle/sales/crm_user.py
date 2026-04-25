from .crm_named_model import CRMNamedModel


class CRMUser(CRMNamedModel):
    email: str | None = None
    phone: str | None = None
