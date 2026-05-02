import psycopg
from psycopg.rows import dict_row

from fluffy_waddle import (
    CRMCampaign,
    CRMContact,
    CRMDeal,
    CRMIndustry,
    CRMLossReason,
    CRMPipeline,
    CRMProduct,
    CRMSource,
)

from assembler import (
    assemble_leaf_map,
    assemble_user_map,
    assemble_pipeline_stage_map,
    assemble_organization_map,
    assemble_deal_contacts_map,
    assemble_deal_products_map,
    assemble_tasks_by_deal_map,
    assemble_deal_map,
)

from deleter import delete_all
from inserter import (
    insert_industries,
    insert_products,
    insert_loss_reasons,
    insert_sources,
    insert_campaigns,
    insert_users,
    insert_teams,
    insert_team_users,
    insert_pipelines,
    insert_pipeline_stages,
    insert_organizations,
    insert_contacts,
    insert_deals,
    insert_deals_products,
    insert_deals_contacts,
    insert_tasks,
    insert_tasks_users,
    insert_organizations_industries,
    insert_organizations_users,
)
from selector import (
    select_industries,
    select_products,
    select_loss_reasons,
    select_sources,
    select_campaigns,
    select_teams,
    select_teams_users,
    select_users,
    select_pipelines,
    select_pipeline_stages,
    select_organizations_industries,
    select_organizations_users,
    select_organizations,
    select_contacts,
    select_deals_contacts,
    select_deals_products,
    select_tasks_users,
    select_tasks,
    select_deals,
)


class DealsRepository:
    def __init__(self, conn: psycopg.Connection):
        self.conn = conn

    def add_deals(self, deals: list[CRMDeal]) -> None:
        with self.conn.transaction():
            with self.conn.cursor() as cur:
                delete_all(cur)

                insert_industries(cur, deals)
                insert_products(cur, deals)
                insert_loss_reasons(cur, deals)
                insert_sources(cur, deals)
                insert_campaigns(cur, deals)
                insert_users(cur, deals)
                insert_teams(cur, deals)
                insert_team_users(cur, deals)
                insert_pipelines(cur, deals)
                insert_pipeline_stages(cur, deals)
                insert_organizations(cur, deals)
                insert_contacts(cur, deals)
                insert_deals(cur, deals)
                insert_deals_products(cur, deals)
                insert_deals_contacts(cur, deals)
                insert_tasks(cur, deals)
                insert_tasks_users(cur, deals)
                insert_organizations_industries(cur, deals)
                insert_organizations_users(cur, deals)

    def get_deals(self) -> list[CRMDeal]:
        with self.conn.cursor(row_factory=dict_row) as cur:
            industry_map = assemble_leaf_map(CRMIndustry, select_industries(cur))
            product_map = assemble_leaf_map(CRMProduct, select_products(cur))
            loss_reason_map = assemble_leaf_map(CRMLossReason, select_loss_reasons(cur))
            source_map = assemble_leaf_map(CRMSource, select_sources(cur))
            campaign_map = assemble_leaf_map(CRMCampaign, select_campaigns(cur))

            user_map = assemble_user_map(
                select_users(cur),
                select_teams(cur),
                select_teams_users(cur),
            )

            pipeline_map = assemble_leaf_map(CRMPipeline, select_pipelines(cur))
            pipeline_stage_map = assemble_pipeline_stage_map(select_pipeline_stages(cur), pipeline_map)

            contact_rows = select_contacts(cur)
            contact_map = assemble_leaf_map(CRMContact, contact_rows)

            organization_map = assemble_organization_map(
                select_organizations(cur),
                user_map,
                industry_map,
                select_organizations_industries(cur),
                select_organizations_users(cur),
                contact_map,
                contact_rows,
            )

            deal_contacts_map = assemble_deal_contacts_map(select_deals_contacts(cur), contact_map)
            deal_products_map = assemble_deal_products_map(select_deals_products(cur), product_map)
            tasks_by_deal_map = assemble_tasks_by_deal_map(
                select_tasks(cur),
                user_map,
                select_tasks_users(cur),
            )

            deal_map = assemble_deal_map(
                select_deals(cur),
                pipeline_stage_map,
                user_map,
                source_map,
                campaign_map,
                loss_reason_map,
                organization_map,
                deal_contacts_map,
                deal_products_map,
                tasks_by_deal_map,
            )

            return list(deal_map.values())
