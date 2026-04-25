from datetime import date, datetime
from decimal import Decimal

import fluffy_waddle
from fluffy_waddle import (
    CRMCampaign,
    CRMContact,
    CRMDeal,
    CRMDealNote,
    CRMDealProduct,
    CRMIndustry,
    CRMLossReason,
    CRMOrganization,
    CRMPipeline,
    CRMPipelineStage,
    CRMProduct,
    CRMTask,
    CRMTeam,
    CRMUser,
    Connection,
    SyncCursor,
)


def test_sales_models_form_a_nested_deal_graph() -> None:
    timestamp = datetime(2026, 1, 1, 12, 0, 0)

    owner = CRMUser(
        id="user-1",
        name="Ada",
        email="ada@example.com",
        created_at=timestamp,
        updated_at=timestamp,
    )
    follower = CRMUser(
        id="user-2",
        name="Grace",
        created_at=timestamp,
        updated_at=timestamp,
    )
    industry = CRMIndustry(
        id="industry-1",
        name="Manufacturing",
        created_at=timestamp,
        updated_at=timestamp,
    )
    pipeline = CRMPipeline(
        id="pipeline-1",
        name="Revenue",
        display_order=1,
        created_at=timestamp,
        updated_at=timestamp,
    )
    stage = CRMPipelineStage(
        id="stage-1",
        name="Qualified",
        pipeline=pipeline,
        display_order=2,
        created_at=timestamp,
        updated_at=timestamp,
    )
    campaign = CRMCampaign(
        id="campaign-1",
        name="Launch",
        description="Q1 launch",
        created_at=timestamp,
        updated_at=timestamp,
    )
    loss_reason = CRMLossReason(
        id="loss-1",
        name="Budget",
        created_at=timestamp,
        updated_at=timestamp,
    )
    organization = CRMOrganization(
        id="org-1",
        name="Acme",
        owner=owner,
        industries=[industry],
        followers=[follower],
        address={"city": "Sao Paulo"},
        created_at=timestamp,
        updated_at=timestamp,
    )
    contact = CRMContact(
        id="contact-1",
        name="Linus",
        organization=organization,
        emails=[{"value": "linus@example.com"}],
        created_at=timestamp,
        updated_at=timestamp,
    )
    product = CRMProduct(
        id="product-1",
        name="Plan",
        price=Decimal("10.00"),
        visible=True,
        created_at=timestamp,
        updated_at=timestamp,
    )
    deal_product = CRMDealProduct(
        id="deal-product-1",
        product=product,
        price=Decimal("10.00"),
        quantity=Decimal("3"),
        total_price=Decimal("30.00"),
        created_at=timestamp,
        updated_at=timestamp,
    )
    deal_note = CRMDealNote(
        id="note-1",
        author=owner,
        edited_by=follower,
        description="Customer requested proposal",
        created_at=timestamp,
    )
    task = CRMTask(
        id="task-1",
        name="Follow up",
        created_by=owner,
        completed_by=follower,
        type="call",
        status="pending",
        assignees=[owner, follower],
        created_at=timestamp,
        updated_at=timestamp,
    )
    deal = CRMDeal(
        id="deal-1",
        name="Expansion",
        stage=stage,
        owner=owner,
        campaign=campaign,
        loss_reason=loss_reason,
        organization=organization,
        contacts=[contact],
        products=[deal_product],
        notes=[deal_note],
        tasks=[task],
        recurrence_price=Decimal("10.00"),
        one_time_price=Decimal("20.00"),
        total_price=Decimal("30.00"),
        expected_close_date=date(2026, 1, 15),
        rating=4,
        status="open",
        distribution_settings={"strategy": "equal"},
        created_at=timestamp,
        updated_at=timestamp,
    )
    team = CRMTeam(
        id="team-1",
        name="Sales",
        members=[owner, follower],
        created_at=timestamp,
        updated_at=timestamp,
    )

    assert deal.stage.pipeline.name == "Revenue"
    assert deal.organization.industries[0].name == "Manufacturing"
    assert deal.contacts[0].organization.owner.name == "Ada"
    assert deal.products[0].product.name == "Plan"
    assert deal.notes[0].author.email == "ada@example.com"
    assert deal.tasks[0].assignees[1].name == "Grace"
    assert team.members[0].name == "Ada"
    assert "stage" in CRMDeal.model_fields
    assert "stage_id" not in CRMDeal.model_fields
    assert "CRMDealContact" not in fluffy_waddle.__all__
    assert "CRMOrganizationIndustry" not in fluffy_waddle.__all__
    assert "CRMSegment" not in fluffy_waddle.__all__
    assert "CRMLostReason" not in fluffy_waddle.__all__


def test_integrations_models_stay_nested_under_connection() -> None:
    timestamp = datetime(2026, 1, 1, 12, 0, 0)

    cursor = SyncCursor(
        id=1,
        resource="deals",
        cursor_type="updated_at",
        cursor={"value": "2026-01-01T00:00:00Z"},
        created_at=timestamp,
        updated_at=timestamp,
    )
    connection = Connection(
        id="conn-1",
        provider="pipedrive",
        account_name="Acme",
        status="connected",
        config={"region": "us"},
        sync_cursors=[cursor],
        created_at=timestamp,
        updated_at=timestamp,
    )

    assert connection.sync_cursors[0].resource == "deals"
    assert connection.config["region"] == "us"
    assert "sync_cursors" in Connection.model_fields
    assert "connection_id" not in SyncCursor.model_fields
