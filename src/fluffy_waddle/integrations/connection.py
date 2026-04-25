from datetime import datetime
from typing import Any
from pydantic import Field
from .integration_model import IntegrationModel
from .sync_cursor import SyncCursor


class Connection(IntegrationModel):
    id: str
    provider: str
    account_name: str
    status: str
    client_id: str | None = None
    client_secret: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_at: datetime | None = None
    reauth_required: bool = False
    redirect_uri: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)
    last_refresh_at: datetime | None = None
    last_refresh_error: str | None = None
    sync_cursors: list[SyncCursor] = Field(default_factory=list)
