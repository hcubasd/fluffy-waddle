import json
from datetime import date, datetime, timezone
from pathlib import Path

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
    CRMSource,
    CRMTask,
    CRMTeam,
    CRMUser,
)


FIXTURE_DIR = Path(__file__).parent / "data"


def load_fixture(name: str) -> dict:
    payload = json.loads((FIXTURE_DIR / name).read_text())
    return payload["data"][0]


def build_user() -> CRMUser:
    return CRMUser.model_validate(load_fixture("users.json"))


def build_campaign() -> CRMCampaign:
    return CRMCampaign.model_validate(load_fixture("campaigns.json"))


def build_industry() -> CRMIndustry:
    return CRMIndustry.model_validate(load_fixture("industries.json"))


def build_loss_reason() -> CRMLossReason:
    return CRMLossReason.model_validate(load_fixture("loss_reasons.json"))


def build_pipeline() -> CRMPipeline:
    payload = load_fixture("pipelines.json")
    return CRMPipeline.model_validate(
        {
            "id": payload["id"],
            "name": payload["name"],
            "display_order": payload["order"],
            "created_at": payload["created_at"],
            "updated_at": payload["updated_at"],
        }
    )


def build_pipeline_stage(pipeline: CRMPipeline) -> CRMPipelineStage:
    payload = load_fixture("pipeline_stages.json")
    return CRMPipelineStage.model_validate(
        {
            "id": payload["id"],
            "name": payload["name"],
            "pipeline": pipeline,
            "description": payload["description"],
            "objective": payload["objective"],
            "display_order": payload["order"],
            "created_at": payload["created_at"],
            "updated_at": payload["updated_at"],
        }
    )


def build_product() -> CRMProduct:
    payload = load_fixture("products.json")
    return CRMProduct.model_validate(
        {
            "id": payload["id"],
            "name": payload["name"],
            "description": payload["description"],
            "price": payload["price"],
            "created_at": payload["created_at"],
            "updated_at": payload["updated_at"],
        }
    )


def build_source() -> CRMSource:
    return CRMSource.model_validate(load_fixture("sources.json"))


def build_contact() -> CRMContact:
    payload = load_fixture("contacts.json")
    return CRMContact.model_validate(
        {
            "id": payload["id"],
            "name": payload["name"],
            "job_title": payload["job_title"],
            "emails": [entry["email"] for entry in payload["emails"]],
            "phones": [entry["phone"] for entry in payload["phones"]],
            "social_profiles": payload["social_profiles"],
            "created_at": payload["created_at"],
            "updated_at": payload["updated_at"],
        }
    )


def build_organization(
    owner: CRMUser,
    industry: CRMIndustry,
    follower: CRMUser,
    contact: CRMContact,
) -> CRMOrganization:
    payload = load_fixture("organizations.json")
    return CRMOrganization.model_validate(
        {
            "id": payload["id"],
            "name": payload["name"],
            "owner": owner,
            "description": payload["description"],
            "url": payload["url"],
            "address": payload["address"],
            "industries": [industry],
            "followers": [follower],
            "contacts": [contact],
            "created_at": payload["created_at"],
            "updated_at": payload["updated_at"],
        }
    )


def build_deal_product(product: CRMProduct) -> CRMDealProduct:
    payload = load_fixture("deal_products.json")
    return CRMDealProduct.model_validate(
        {
            "id": payload["id"],
            "product": product,
            "price": payload["price"],
            "quantity": payload["quantity"],
            "discount_type": payload["discount_type"],
            "discount": payload["discount"],
            "total_price": payload["total_price"],
            "billing_frequency": payload["billing_frequency"],
            "created_at": payload["created_at"],
            "updated_at": payload["updated_at"],
        }
    )


def build_deal_note(author: CRMUser, editor: CRMUser) -> CRMDealNote:
    payload = load_fixture("deal_notes.json")
    return CRMDealNote.model_validate(
        {
            "id": payload["id"],
            "author": author,
            "description": payload["description"],
            "created_at": payload["registered_at"],
            "pinned_at": payload["pinned_at"],
            "edited_by": editor,
            "edited_at": payload["edited_at"],
        }
    )


def build_task(created_by: CRMUser, completed_by: CRMUser) -> CRMTask:
    payload = load_fixture("tasks.json")
    return CRMTask.model_validate(
        {
            "id": payload["id"],
            "name": payload["name"],
            "description": payload["description"],
            "type": payload["type"],
            "status": payload["status"],
            "due_date": payload["due_date"],
            "created_by": created_by,
            "completed_by": completed_by,
            "completed_at": payload["completed_at"],
            "assignees": [created_by],
            "created_at": payload["created_at"],
            "updated_at": payload["updated_at"],
        }
    )


def build_team(member: CRMUser) -> CRMTeam:
    payload = load_fixture("teams.json")
    return CRMTeam.model_validate(
        {
            "id": payload["team_id"],
            "name": payload["name"],
            "members": [member],
            "created_at": payload["created_at"],
            "updated_at": payload["updated_at"],
        }
    )


def build_deal(
    stage: CRMPipelineStage,
    owner: CRMUser,
    source: CRMSource,
    campaign: CRMCampaign,
    loss_reason: CRMLossReason,
    organization: CRMOrganization,
    contact: CRMContact,
    deal_product: CRMDealProduct,
    deal_note: CRMDealNote,
    task: CRMTask,
) -> CRMDeal:
    payload = load_fixture("deals.json")
    return CRMDeal.model_validate(
        {
            "id": payload["id"],
            "name": payload["name"],
            "stage": stage,
            "owner": owner,
            "source": source,
            "campaign": campaign,
            "loss_reason": loss_reason,
            "organization": organization,
            "expected_close_date": payload["expected_close_date"],
            "rating": payload["rating"],
            "status": payload["status"],
            "closed_at": payload["closed_at"],
            "contacts": [contact],
            "deal_products": [deal_product],
            "notes": [deal_note],
            "tasks": [task],
            "created_at": payload["created_at"],
            "updated_at": payload["updated_at"],
        }
    )


def test_reference_models_load_from_fixtures() -> None:
    user = build_user()
    campaign = build_campaign()
    industry = build_industry()
    loss_reason = build_loss_reason()
    pipeline = build_pipeline()
    stage = build_pipeline_stage(pipeline)
    product = build_product()
    source = build_source()

    assert user.email == "string"
    assert campaign.description == "string"
    assert industry.name == "string"
    assert loss_reason.id == "string"
    assert pipeline.display_order == 0
    assert stage.pipeline is pipeline
    assert stage.display_order == 0
    assert product.price == 0
    assert source.name == "string"


def test_organization_graph_loads_from_fixtures() -> None:
    owner = build_user()
    industry = build_industry()
    follower = build_user()
    contact = build_contact()
    organization = build_organization(owner, industry, follower, contact)
    team = build_team(owner)

    assert organization.owner is owner
    assert organization.industries[0] is industry
    assert organization.followers[0].name == "string"
    assert organization.contacts[0].emails == ["string"]
    assert organization.contacts[0].phones == ["string"]
    assert organization.address["line"] == "string"
    assert team.id == "string"
    assert team.members[0] is owner


def test_deal_graph_loads_from_fixtures() -> None:
    owner = build_user()
    pipeline = build_pipeline()
    stage = build_pipeline_stage(pipeline)
    campaign = build_campaign()
    loss_reason = build_loss_reason()
    source = build_source()
    contact = build_contact()
    organization = build_organization(owner, build_industry(), build_user(), contact)
    deal_product = build_deal_product(build_product())
    deal_note = build_deal_note(owner, owner)
    task = build_task(owner, owner)
    deal = build_deal(
        stage,
        owner,
        source,
        campaign,
        loss_reason,
        organization,
        contact,
        deal_product,
        deal_note,
        task,
    )

    assert deal.stage.pipeline.display_order == 0
    assert deal.owner.phone == "string"
    assert deal.source.description == "string"
    assert deal.campaign.name == "string"
    assert deal.loss_reason.name == "string"
    assert deal.organization.contacts[0].job_title == "string"
    assert deal.contacts[0].social_profiles[0]["type"] == "facebook"
    assert deal.deal_products[0].product.description == "string"
    assert deal.deal_products[0].billing_frequency == "one-time"
    assert deal.notes[0].author.id == "string"
    assert deal.expected_close_date == date(2026, 4, 24)
    assert deal.notes[0].created_at == datetime(2026, 4, 24, 22, 9, 5, 6000, tzinfo=timezone.utc)
    assert deal.tasks[0].created_by is owner
    assert deal.tasks[0].assignees[0] is owner
    assert deal.status == "won"
