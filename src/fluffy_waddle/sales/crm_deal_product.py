from decimal import Decimal
from .crm_model import CRMModel
from .crm_product import CRMProduct

class CRMDealProduct(CRMModel):
    product: CRMProduct
    price: Decimal
    quantity: Decimal
    discount_type: str | None = None
    discount: Decimal = Decimal(0)
    total_price: Decimal
    billing_frequency: str | None = None
