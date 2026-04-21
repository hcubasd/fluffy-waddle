from decimal import Decimal
from typing import Optional
from .crm_named_model import CRMNamedModel


class CRMProduct(CRMNamedModel):
    description: Optional[str] = None
    price: Decimal
    visible: bool
