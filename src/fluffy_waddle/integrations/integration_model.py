from datetime import datetime
from pydantic import BaseModel


class IntegrationModel(BaseModel):
    created_at: datetime
    updated_at: datetime
