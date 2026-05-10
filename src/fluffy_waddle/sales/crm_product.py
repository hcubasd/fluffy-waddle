from decimal import Decimal
from .crm_named_model import CRMNamedModel


class CRMProduct(CRMNamedModel):
    description: str | None = None
    price: Decimal
