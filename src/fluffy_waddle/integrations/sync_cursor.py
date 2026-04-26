from datetime import datetime
from typing import Any
from pydantic import Field
from .integration_model import IntegrationModel

class SyncCursor(IntegrationModel):
    id: int
    resource: str
    cursor_type: str
    cursor: dict[str, Any] = Field(default_factory=dict)
    last_sync_at: datetime | None = None
    last_sync_status: str | None = None
    last_error: str | None = None
