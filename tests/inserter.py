import psycopg
from psycopg.types.json import Jsonb

from fluffy_waddle import CRMDeal


def _industry_rows(deals: list[CRMDeal]):
    return [
        i.model_dump()
            for d in deals if d.organization
                for i in d.organization.industries
    ]

def insert_industries(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_industries (
            id,
            name,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(name)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _industry_rows(deals))

def _product_rows(deals: list[CRMDeal]):
    return [
        p.model_dump()
            for d in deals
                for p in d.products
    ]

def insert_products(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_products (
            id,
            name,
            description,
            price,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(name)s,
            %(description)s,
            %(price)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _product_rows(deals))

def _loss_reason_rows(deals: list[CRMDeal]):
    return [
        d.loss_reason.model_dump()
            for d in deals if d.loss_reason
    ]

def insert_loss_reasons(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_loss_reasons (
            id,
            name,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(name)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _loss_reason_rows(deals))

def _source_rows(deals: list[CRMDeal]):
    return [
        d.source.model_dump()
            for d in deals if d.source
    ]

def insert_sources(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_sources (
            id,
            name,
            description,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(name)s,
            %(description)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _source_rows(deals))

def _campaign_rows(deals: list[CRMDeal]):
    return [
        d.campaign.model_dump()
            for d in deals if d.campaign
    ]

def insert_campaigns(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_campaigns (
            id,
            name,
            description,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(name)s,
            %(description)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _campaign_rows(deals))

def _all_deal_users(deals: list[CRMDeal]):
    for d in deals:
        if d.owner:
            yield d.owner
        if d.organization:
            if d.organization.owner:
                yield d.organization.owner
            yield from d.organization.followers
        for t in d.tasks:
            yield t.created_by
            if t.completed_by:
                yield t.completed_by
            yield from t.assignees

def _user_rows(deals: list[CRMDeal]):
    return [u.model_dump() for u in _all_deal_users(deals)]

def insert_users(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_users (
            id,
            name,
            email,
            phone,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(name)s,
            %(email)s,
            %(phone)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _user_rows(deals))

def _team_rows(deals: list[CRMDeal]):
    return [
        u.team.model_dump()
            for u in _all_deal_users(deals) if u.team
    ]

def insert_teams(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_teams (
            id,
            name,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(name)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _team_rows(deals))

def _team_user_rows(deals: list[CRMDeal]):
    return [
        {"team_id": u.team.id, "user_id": u.id}
            for u in _all_deal_users(deals) if u.team
    ]

def insert_team_users(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_teams_users (
            team_id,
            user_id
        ) VALUES (
            %(team_id)s,
            %(user_id)s
        ) ON CONFLICT DO NOTHING
    """, _team_user_rows(deals))

def _pipeline_rows(deals: list[CRMDeal]):
    return [
        d.stage.pipeline.model_dump()
            for d in deals
    ]

def insert_pipelines(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_pipelines (
            id,
            name,
            display_order,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(name)s,
            %(display_order)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _pipeline_rows(deals))

def _pipeline_stage_rows(deals: list[CRMDeal]):
    return [
        {**d.stage.model_dump(), "pipeline_id": d.stage.pipeline.id}
            for d in deals
    ]

def insert_pipeline_stages(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_pipeline_stages (
            id,
            pipeline_id,
            name,
            description,
            objective,
            display_order,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(pipeline_id)s,
            %(name)s,
            %(description)s,
            %(objective)s,
            %(display_order)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _pipeline_stage_rows(deals))

def _organization_rows(deals: list[CRMDeal]):
    return [
        {
            **d.organization.model_dump(),
            "owner_id": d.organization.owner.id if d.organization.owner else None,
            "address": Jsonb(d.organization.address) if d.organization.address else None,
        }
            for d in deals if d.organization
    ]

def insert_organizations(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_organizations (
            id,
            owner_id,
            name,
            description,
            url,
            address,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(owner_id)s,
            %(name)s,
            %(description)s,
            %(url)s,
            %(address)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _organization_rows(deals))

def _contact_rows(deals: list[CRMDeal]):
    rows = []
    for d in deals:
        if d.organization:
            for c in d.organization.contacts:
                rows.append({
                    **c.model_dump(),
                    "organization_id": d.organization.id,
                    "emails": Jsonb(c.emails),
                    "phones": Jsonb(c.phones),
                    "social_profiles": Jsonb(c.social_profiles),
                })
        for c in d.contacts:
            rows.append({
                **c.model_dump(),
                "organization_id": None,
                "emails": Jsonb(c.emails),
                "phones": Jsonb(c.phones),
                "social_profiles": Jsonb(c.social_profiles),
            })
    return rows

def insert_contacts(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_contacts (
            id,
            organization_id,
            name,
            job_title,
            emails,
            phones,
            social_profiles,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(organization_id)s,
            %(name)s,
            %(job_title)s,
            %(emails)s,
            %(phones)s,
            %(social_profiles)s,
            %(created_at)s,
            %(updated_at)s
        ) ON CONFLICT DO NOTHING
    """, _contact_rows(deals))

def _deal_rows(deals: list[CRMDeal]):
    return [
        {
            **d.model_dump(),
            "stage_id": d.stage.id,
            "owner_id": d.owner.id if d.owner else None,
            "source_id": d.source.id if d.source else None,
            "campaign_id": d.campaign.id if d.campaign else None,
            "loss_reason_id": d.loss_reason.id if d.loss_reason else None,
            "organization_id": d.organization.id if d.organization else None,
        }
            for d in deals
    ]

def insert_deals(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_deals (
            id,
            stage_id,
            owner_id,
            source_id,
            campaign_id,
            loss_reason_id,
            organization_id,
            name,
            value,
            expected_close_date,
            rating,
            status,
            closed_at,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(stage_id)s,
            %(owner_id)s,
            %(source_id)s,
            %(campaign_id)s,
            %(loss_reason_id)s,
            %(organization_id)s,
            %(name)s,
            %(value)s,
            %(expected_close_date)s,
            %(rating)s,
            %(status)s,
            %(closed_at)s,
            %(created_at)s,
            %(updated_at)s
        )
    """, _deal_rows(deals))

def _deals_product_rows(deals: list[CRMDeal]):
    return [
        {"deal_id": d.id, "product_id": p.id}
            for d in deals
                for p in d.products
    ]

def insert_deals_products(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_deals_products (
            deal_id,
            product_id
        ) VALUES (
            %(deal_id)s,
            %(product_id)s
        ) ON CONFLICT DO NOTHING
    """, _deals_product_rows(deals))

def _deals_contact_rows(deals: list[CRMDeal]):
    return [
        {"deal_id": d.id, "contact_id": c.id}
            for d in deals
                for c in d.contacts
    ]

def insert_deals_contacts(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_deals_contacts (
            deal_id,
            contact_id
        ) VALUES (
            %(deal_id)s,
            %(contact_id)s
        )
    """, _deals_contact_rows(deals))

def _task_rows(deals: list[CRMDeal]):
    return [
        {
            **t.model_dump(),
            "created_by_id": t.created_by.id,
            "completed_by_id": t.completed_by.id if t.completed_by else None,
            "deal_id": d.id,
        }
            for d in deals if d.tasks
                for t in d.tasks
    ]

def insert_tasks(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_tasks (
            id,
            created_by_id,
            completed_by_id,
            deal_id,
            name,
            description,
            type,
            status,
            due_date,
            completed_at,
            created_at,
            updated_at
        ) VALUES (
            %(id)s,
            %(created_by_id)s,
            %(completed_by_id)s,
            %(deal_id)s,
            %(name)s,
            %(description)s,
            %(type)s,
            %(status)s,
            %(due_date)s,
            %(completed_at)s,
            %(created_at)s,
            %(updated_at)s
        )
    """, _task_rows(deals))

def _tasks_user_rows(deals: list[CRMDeal]):
    return [
        {"task_id": t.id, "user_id": u.id}
            for d in deals if d.tasks
                for t in d.tasks
                    for u in t.assignees
    ]

def insert_tasks_users(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_tasks_users (
            task_id,
            user_id
        ) VALUES (
            %(task_id)s,
            %(user_id)s
        )
    """, _tasks_user_rows(deals))

def _organizations_industry_rows(deals: list[CRMDeal]):
    return [
        {"organization_id": d.organization.id, "industry_id": i.id}
            for d in deals if d.organization
                for i in d.organization.industries
    ]

def insert_organizations_industries(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_organizations_industries (
            organization_id,
            industry_id
        ) VALUES (
            %(organization_id)s,
            %(industry_id)s
        )
    """, _organizations_industry_rows(deals))

def _organizations_user_rows(deals: list[CRMDeal]):
    return [
        {"organization_id": d.organization.id, "user_id": u.id}
            for d in deals if d.organization
                for u in d.organization.followers
    ]

def insert_organizations_users(cur: psycopg.Cursor, deals: list[CRMDeal]):
    cur.executemany("""
        INSERT INTO sales.crm_organizations_users (
            organization_id,
            user_id
        ) VALUES (
            %(organization_id)s,
            %(user_id)s
        )
    """, _organizations_user_rows(deals))
