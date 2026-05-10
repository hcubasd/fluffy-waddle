import psycopg
from psycopg.rows import dict_row

from fluffy_waddle.sales import (
    CRMCampaign,
    CRMContact,
    CRMDeal,
    CRMIndustry,
    CRMLossReason,
    CRMPipeline,
    CRMProduct,
    CRMSource,
)

from deals_assembler import (
    assemble_deal_contacts_map,
    assemble_deal_map,
    assemble_deal_products_map,
    assemble_leaf_map,
    assemble_organization_map,
    assemble_pipeline_stage_map,
    assemble_tasks_by_deal_map,
    assemble_user_map,
)
from deleter import delete_all
from inserters import (
    all_users,
    insert_contacts,
    insert_deals,
    insert_join,
    insert_named,
    insert_named_described,
    insert_organizations,
    insert_pipeline_stages,
    insert_pipelines,
    insert_products,
    insert_tasks,
    insert_users,
)
from db_selectors import select_all, select_join


class DealsRepository:
    def __init__(self, conn: psycopg.Connection):
        self.conn = conn

    def add_deals(self, deals: list[CRMDeal]) -> None:
        with self.conn.transaction():
            with self.conn.cursor() as cur:
                delete_all(cur)

                users = list(all_users(deals))

                insert_named(
                    cur,
                    "crm_industries",
                    [
                        i.model_dump()
                        for d in deals
                        if d.organization
                        for i in d.organization.industries
                    ],
                )
                insert_products(cur, deals)
                insert_named(
                    cur,
                    "crm_loss_reasons",
                    [d.loss_reason.model_dump() for d in deals if d.loss_reason],
                )
                insert_named_described(
                    cur,
                    "crm_sources",
                    [d.source.model_dump() for d in deals if d.source],
                )
                insert_named_described(
                    cur,
                    "crm_campaigns",
                    [d.campaign.model_dump() for d in deals if d.campaign],
                )
                insert_users(cur, users)
                insert_named(
                    cur, "crm_teams", [u.team.model_dump() for u in users if u.team]
                )
                insert_join(
                    cur,
                    "crm_teams_users",
                    "team_id",
                    "user_id",
                    [(u.team.id, u.id) for u in users if u.team],
                )
                insert_pipelines(cur, deals)
                insert_pipeline_stages(cur, deals)
                insert_organizations(cur, deals)
                insert_join(
                    cur,
                    "crm_organizations_industries",
                    "organization_id",
                    "industry_id",
                    [
                        (d.organization.id, i.id)
                        for d in deals
                        if d.organization
                        for i in d.organization.industries
                    ],
                )
                insert_join(
                    cur,
                    "crm_organizations_users",
                    "organization_id",
                    "user_id",
                    [
                        (d.organization.id, u.id)
                        for d in deals
                        if d.organization
                        for u in d.organization.followers
                    ],
                )
                insert_contacts(cur, deals)
                insert_deals(cur, deals)
                insert_join(
                    cur,
                    "crm_deals_products",
                    "deal_id",
                    "product_id",
                    [(d.id, p.id) for d in deals for p in d.products],
                )
                insert_join(
                    cur,
                    "crm_deals_contacts",
                    "deal_id",
                    "contact_id",
                    [(d.id, c.id) for d in deals for c in d.contacts],
                )
                insert_tasks(cur, deals)
                insert_join(
                    cur,
                    "crm_tasks_users",
                    "task_id",
                    "user_id",
                    [(t.id, u.id) for d in deals for t in d.tasks for u in t.assignees],
                )

    def get_deals(self) -> list[CRMDeal]:
        with self.conn.cursor(row_factory=dict_row) as cur:
            industry_map = assemble_leaf_map(
                CRMIndustry, select_all(cur, "crm_industries")
            )
            product_map = assemble_leaf_map(CRMProduct, select_all(cur, "crm_products"))
            loss_reason_map = assemble_leaf_map(
                CRMLossReason, select_all(cur, "crm_loss_reasons")
            )
            source_map = assemble_leaf_map(CRMSource, select_all(cur, "crm_sources"))
            campaign_map = assemble_leaf_map(
                CRMCampaign, select_all(cur, "crm_campaigns")
            )

            user_map = assemble_user_map(
                select_all(cur, "crm_users"),
                select_all(cur, "crm_teams"),
                select_join(cur, "crm_teams_users", "team_id", "user_id"),
            )

            pipeline_map = assemble_leaf_map(
                CRMPipeline, select_all(cur, "crm_pipelines")
            )
            pipeline_stage_map = assemble_pipeline_stage_map(
                select_all(cur, "crm_pipeline_stages"), pipeline_map
            )

            contact_rows = select_all(cur, "crm_contacts")
            contact_map = assemble_leaf_map(CRMContact, contact_rows)

            organization_map = assemble_organization_map(
                select_all(cur, "crm_organizations"),
                user_map,
                industry_map,
                select_join(
                    cur,
                    "crm_organizations_industries",
                    "organization_id",
                    "industry_id",
                ),
                select_join(
                    cur, "crm_organizations_users", "organization_id", "user_id"
                ),
                contact_map,
                contact_rows,
            )

            deal_contacts_map = assemble_deal_contacts_map(
                select_join(cur, "crm_deals_contacts", "deal_id", "contact_id"),
                contact_map,
            )
            deal_products_map = assemble_deal_products_map(
                select_join(cur, "crm_deals_products", "deal_id", "product_id"),
                product_map,
            )
            tasks_by_deal_map = assemble_tasks_by_deal_map(
                select_all(cur, "crm_tasks"),
                user_map,
                select_join(cur, "crm_tasks_users", "task_id", "user_id"),
            )

            return list(
                assemble_deal_map(
                    select_all(cur, "crm_deals"),
                    pipeline_stage_map,
                    user_map,
                    source_map,
                    campaign_map,
                    loss_reason_map,
                    organization_map,
                    deal_contacts_map,
                    deal_products_map,
                    tasks_by_deal_map,
                ).values()
            )
