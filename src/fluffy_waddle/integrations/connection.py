from datetime import datetime
from typing import Optional
from .integration_model import IntegrationModel
from .sync_cursor import SyncCursor


class Connection(IntegrationModel):
    id: str
    provider: str
    account_name: str
    status: str
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_at: Optional[datetime] = None
    reauth_required: bool = False
    redirect_uri: Optional[str] = None
    config: dict = {}
    last_refresh_at: Optional[datetime] = None
    last_refresh_error: Optional[str] = None
    sync_cursors: list[SyncCursor] = []
