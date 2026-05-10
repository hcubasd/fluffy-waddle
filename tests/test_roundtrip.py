from datetime import date, datetime, timezone
from decimal import Decimal

import psycopg

from fluffy_waddle.sales import (
    CRMCampaign,
    CRMContact,
    CRMDeal,
    CRMIndustry,
    CRMLossReason,
    CRMOrganization,
    CRMPipeline,
    CRMPipelineStage,
    CRMProduct,
    CRMSource,
    CRMTask,
    CRMTeam,
    CRMUser,
)

from deals_repository import DealsRepository

_NOW = datetime(2024, 1, 1, tzinfo=timezone.utc)

_team = CRMTeam(id="t1", name="Sales", created_at=_NOW, updated_at=_NOW)
_user = CRMUser(
    id="u1",
    name="Alice",
    email="alice@example.com",
    phone=None,
    team=_team,
    created_at=_NOW,
    updated_at=_NOW,
)
_pipeline = CRMPipeline(
    id="pl1", name="Main", display_order=1, created_at=_NOW, updated_at=_NOW
)
_stage = CRMPipelineStage(
    id="ps1",
    name="Proposal",
    pipeline=_pipeline,
    display_order=1,
    description=None,
    objective=None,
    created_at=_NOW,
    updated_at=_NOW,
)
_industry = CRMIndustry(id="ind1", name="Tech", created_at=_NOW, updated_at=_NOW)
_source = CRMSource(
    id="src1", name="Web", description=None, created_at=_NOW, updated_at=_NOW
)
_campaign = CRMCampaign(
    id="cmp1", name="Q1", description=None, created_at=_NOW, updated_at=_NOW
)
_loss_reason = CRMLossReason(id="lr1", name="Price", created_at=_NOW, updated_at=_NOW)
_product = CRMProduct(
    id="pr1",
    name="Widget",
    description=None,
    price=Decimal("99.99"),
    created_at=_NOW,
    updated_at=_NOW,
)
_contact = CRMContact(
    id="ct1", name="Bob", job_title="CEO", created_at=_NOW, updated_at=_NOW
)
_org = CRMOrganization(
    id="org1",
    name="Acme",
    owner=_user,
    description=None,
    url=None,
    address=None,
    industries=[_industry],
    followers=[_user],
    contacts=[_contact],
    created_at=_NOW,
    updated_at=_NOW,
)
_task = CRMTask(
    id="tk1",
    name="Follow up",
    type="call",
    status="pending",
    created_by=_user,
    completed_by=None,
    description=None,
    due_date=None,
    completed_at=None,
    assignees=[_user],
    created_at=_NOW,
    updated_at=_NOW,
)

DEALS = [
    CRMDeal(
        id="d1",
        name="Big Deal",
        stage=_stage,
        owner=_user,
        source=_source,
        campaign=_campaign,
        loss_reason=_loss_reason,
        organization=_org,
        value=Decimal("10000.00"),
        expected_close_date=date(2024, 3, 31),
        rating=3,
        status="ongoing",
        closed_at=None,
        contacts=[_contact],
        products=[_product],
        tasks=[_task],
        created_at=_NOW,
        updated_at=_NOW,
    )
]


def _sort_key(value):
    if isinstance(value, dict):
        return (value.get("id") is None, value.get("id"), repr(value))
    return (False, None, repr(value))


def _normalize(value):
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return sorted((_normalize(v) for v in value), key=_sort_key)
    return value


def test_roundtrip():
    with psycopg.connect() as conn:
        repo = DealsRepository(conn)
        repo.add_deals(DEALS)
        result = repo.get_deals()

    assert [_normalize(d.model_dump()) for d in result] == [
        _normalize(d.model_dump()) for d in DEALS
    ]
