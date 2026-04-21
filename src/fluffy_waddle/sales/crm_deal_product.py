from decimal import Decimal
from typing import Optional
from .crm_model import CRMModel
from .crm_product import CRMProduct


class CRMDealProduct(CRMModel):
    deal_id: str
    product: CRMProduct
    price: Decimal
    quantity: Decimal
    discount_type: Optional[str] = None
    discount: Decimal = Decimal("0")
    total_price: Decimal
    billing_frequency: Optional[str] = None
