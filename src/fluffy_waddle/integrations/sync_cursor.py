from datetime import datetime
from typing import Optional
from .integration_model import IntegrationModel


class SyncCursor(IntegrationModel):
    id: int
    connection_id: str
    resource: str
    cursor_type: str
    cursor: dict = {}
    last_sync_at: Optional[datetime] = None
    last_sync_status: Optional[str] = None
    last_error: Optional[str] = None
