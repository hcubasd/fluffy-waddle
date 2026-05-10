import psycopg

from fluffy_waddle import (
    CRMContact,
    CRMDeal,
    CRMOrganization,
    CRMPipeline,
    CRMPipelineStage,
    CRMTask,
    CRMTeam,
    CRMUser,
)


def assemble_leaf_map(Model, rows):
    return {r["id"]: Model(**r) for r in rows}


def assemble_user_map(users_rows, teams_rows, teams_users_rows):
    try:
        teams = {r["id"]: CRMTeam(**r) for r in teams_rows}

        user_team_map = {
            r["user_id"]: teams[r["team_id"]]
            for r in teams_users_rows
            if r["team_id"] in teams
        }

        return {
            r["id"]: CRMUser(**{**r, "team": user_team_map.get(r["id"])})
            for r in users_rows
        }
    except Exception as e:
        raise Exception("Error assembling users") from e


def assemble_pipeline_stage_map(rows, pipeline_map):
    try:
        return {
            r["id"]: CRMPipelineStage(
                **{**r, "pipeline": pipeline_map[r["pipeline_id"]]}
            )
            for r in rows
        }
    except Exception as e:
        raise Exception("Error assembling pipeline stages") from e


def assemble_organization_map(
    orgs_rows,
    users_map,
    industries_map,
    org_industries_rows,
    org_followers_rows,
    contact_map,
    contact_rows,
):
    try:
        org_industries: dict[str, list] = {}
        for r in org_industries_rows:
            if r["industry_id"] in industries_map:
                org_industries.setdefault(r["organization_id"], []).append(
                    industries_map[r["industry_id"]]
                )

        org_followers: dict[str, list] = {}
        for r in org_followers_rows:
            if r["user_id"] in users_map:
                org_followers.setdefault(r["organization_id"], []).append(
                    users_map[r["user_id"]]
                )

        org_contacts: dict[str, list] = {}
        for r in contact_rows:
            if r.get("organization_id") and r["id"] in contact_map:
                org_contacts.setdefault(r["organization_id"], []).append(
                    contact_map[r["id"]]
                )

        return {
            r["id"]: CRMOrganization(
                **{
                    **r,
                    "owner": users_map.get(r["owner_id"]) if r["owner_id"] else None,
                    "industries": org_industries.get(r["id"], []),
                    "followers": org_followers.get(r["id"], []),
                    "contacts": org_contacts.get(r["id"], []),
                }
            )
            for r in orgs_rows
        }
    except Exception as e:
        raise Exception("Error assembling organizations") from e


def assemble_deal_contacts_map(deals_contacts_rows, contacts_map):
    deal_contacts: dict[str, list] = {}

    for r in deals_contacts_rows:
        if r["contact_id"] in contacts_map:
            deal_contacts.setdefault(r["deal_id"], []).append(
                contacts_map[r["contact_id"]]
            )

    return deal_contacts


def assemble_deal_products_map(deals_products_rows, products_map):
    deal_products: dict[str, list] = {}

    for r in deals_products_rows:
        if r["product_id"] in products_map:
            deal_products.setdefault(r["deal_id"], []).append(
                products_map[r["product_id"]]
            )

    return deal_products


def assemble_tasks_by_deal_map(tasks_rows, users_map, tasks_users_rows):
    try:
        task_assignees: dict[str, list] = {}
        for r in tasks_users_rows:
            if r["user_id"] in users_map:
                task_assignees.setdefault(r["task_id"], []).append(
                    users_map[r["user_id"]]
                )

        tasks_by_deal: dict[str, list] = {}
        for r in tasks_rows:
            t = CRMTask(
                **{
                    **r,
                    "created_by": users_map[r["created_by_id"]],
                    "completed_by": users_map.get(r["completed_by_id"])
                    if r["completed_by_id"]
                    else None,
                    "assignees": task_assignees.get(r["id"], []),
                }
            )
            if r["deal_id"]:
                tasks_by_deal.setdefault(r["deal_id"], []).append(t)

        return tasks_by_deal
    except Exception as e:
        raise Exception("Error assembling tasks") from e


def assemble_deal_map(
    deals_rows,
    pipeline_stage_map,
    users_map,
    sources_map,
    campaigns_map,
    loss_reasons_map,
    organizations_map,
    deal_contacts_map,
    deal_products_map,
    tasks_by_deal_map,
):
    try:
        deals = [
            CRMDeal(
                **{
                    **r,
                    "stage": pipeline_stage_map[r["stage_id"]],
                    "owner": users_map.get(r["owner_id"]) if r["owner_id"] else None,
                    "source": sources_map.get(r["source_id"])
                    if r["source_id"]
                    else None,
                    "campaign": campaigns_map.get(r["campaign_id"])
                    if r["campaign_id"]
                    else None,
                    "loss_reason": loss_reasons_map.get(r["loss_reason_id"])
                    if r["loss_reason_id"]
                    else None,
                    "organization": organizations_map.get(r["organization_id"])
                    if r["organization_id"]
                    else None,
                    "contacts": deal_contacts_map.get(r["id"], []),
                    "products": deal_products_map.get(r["id"], []),
                    "tasks": tasks_by_deal_map.get(r["id"], []),
                }
            )
            for r in deals_rows
        ]

        return {deal.id: deal for deal in deals}
    except Exception as e:
        raise Exception("Error assembling deals") from e
