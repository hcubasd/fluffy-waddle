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

def make_leaf_map(Model, leaf_data):
    leaves = [
        Model.model_validate(item)
            for item in leaf_data["data"]
    ]

    return {
        leaf.id: leaf
            for leaf in leaves
    }

def make_pipeline_map(pipeline_data):
    pipelines = [
        CRMPipeline.model_validate({
            **pipeline,
            "display_order": pipeline["order"]                               
        }) for pipeline in pipeline_data["data"]
    ]

    return {
        pipeline.id: pipeline
            for pipeline in pipelines
    }

def make_team_map(team_data):
    teams = [
        CRMTeam.model_validate({
            **team,
            "id": team["team_id"]
        }) for team in team_data["data"]
    ]

    return {
        team.id: team
            for team in teams
    }

def make_pipeline_stage_map(pipeline_stage_data, pipeline_map):
    try:
        pipeline_stages = [
            CRMPipelineStage.model_validate({
                **stage,
                "display_order": stage["order"],
                "pipeline": pipeline_map[stage["pipeline_id"]],
            }) for stage in pipeline_stage_data["data"]
        ]

        return {
            pipeline_stage.id: pipeline_stage
                for pipeline_stage in pipeline_stages
        }
    except Exception as e:
        raise Exception("Error parsing pipeline stages data") from e

def make_user_map(user_data, team_data, team_map):
    try:
        user_team_map = {
            user_id: team_map[raw["team_id"]]
                for raw in team_data["data"]
                    if raw["team_id"] in team_map
                        for user_id in raw.get("user_ids", [])
        }

        users = [
            CRMUser.model_validate({
                **user,
                "team": user_team_map.get(user["id"]),
            }) for user in user_data["data"]
        ]

        return {
            user.id: user
                for user in users
        }
    except Exception as e:
        raise Exception("Error parsing users data") from e

def make_organization_map(
    organization_data,
    user_map,
    industry_map,
    contact_data,
     contact_map
 ):
    try:
        org_contacts_map: dict[str, list] = {}
        for raw in contact_data["data"]:
            org_id = raw.get("organization_id")
            if org_id and raw["id"] in contact_map:
                org_contacts_map.setdefault(org_id, []).append(contact_map[raw["id"]])

        organizations = [
            CRMOrganization.model_validate({
                **org,
                "owner": user_map.get(org.get("owner_id")),
                "industries": [
                    industry_map[i]
                        for i in org.get("segment_ids", []) if i in industry_map
                ],
                "followers": [
                    user_map[i]
                        for i in org.get("follower_ids", []) if i in user_map
                ],
                "contacts": org_contacts_map.get(org["id"], []),
            }) for org in organization_data["data"]
        ]

        return {
            organization.id: organization
                for organization in organizations
        }
    except Exception as e:
        raise Exception("Error parsing organizations data") from e

def make_tasks_by_deal_map(task_data, user_map):
    try:
        tasks_by_deal: dict[str, list] = {}

        for raw in task_data["data"]:
            task = CRMTask.model_validate({
                **raw,
                "created_by": user_map[raw["created_by_id"]],
                "completed_by": user_map.get(raw.get("completed_by_id")),
                "assignees": [
                    user_map[i] for i in raw.get("owner_ids", []) if i in user_map
                ],
            })
            if raw.get("deal_id"):
                tasks_by_deal.setdefault(raw["deal_id"], []).append(task)

        return tasks_by_deal
    except Exception as e:
        raise Exception("Error parsing tasks data") from e

def make_deal_products_map(deal_data, product_map):
    deal_products: dict[str, list] = {
        deal["id"]: [] for deal in deal_data["data"]
    }

    for product in product_map.values():
        for deal in deal_data["data"]:
            deal_products[deal["id"]].append(product)

    return deal_products

def make_campaign_map(campaign_data):
    return make_leaf_map(CRMCampaign, campaign_data)

def make_deal_map(
    deal_data,
    pipeline_stage_map,
    user_map,
    source_map,
    campaign_map,
    loss_reason_map,
    organization_map,
    contact_map,
    deal_products_map,
    tasks_by_deal_map
):
    try:
        deals = [
            CRMDeal.model_validate({
                **deal,
                "stage": pipeline_stage_map[deal["stage_id"]],
                "owner": user_map.get(deal.get("owner_id")),
                "source": source_map.get(deal.get("source_id")),
                "campaign": campaign_map.get(deal.get("campaign_id")),
                "loss_reason": loss_reason_map.get(deal.get("lost_reason_id")),
                "organization": organization_map.get(deal.get("organization_id")),
                "value": deal.get("total_price"),
                "contacts": [
                    contact_map[i] for i in deal.get("contact_ids", []) if i in contact_map
                ],
                "products": deal_products_map.get(deal["id"], []),
                "tasks": tasks_by_deal_map.get(deal["id"], []),
            }) for deal in deal_data["data"]
        ]

        return {
            deal.id: deal
                for deal in deals
        }
    except Exception as e:
        raise Exception("Error parsing deals data") from e

def make_deals(
    campaigns_data,
    contacts_data,
    deals_data,
    industries_data,
    loss_reasons_data,
    organizations_data,
    pipeline_stages_data,
    pipelines_data,
    products_data,
    sources_data,
    tasks_data,
    teams_data,
    users_data,
):
    industry_map = make_leaf_map(CRMIndustry, industries_data)
    product_map = make_leaf_map(CRMProduct, products_data)
    loss_reason_map = make_leaf_map(CRMLossReason, loss_reasons_data)
    source_map = make_leaf_map(CRMSource, sources_data)
    campaign_map = make_campaign_map(campaigns_data)

    team_map = make_team_map(teams_data)
    user_map = make_user_map(users_data, teams_data, team_map)

    pipeline_map = make_pipeline_map(pipelines_data)
    pipeline_stage_map = make_pipeline_stage_map(pipeline_stages_data, pipeline_map)

    contact_map = make_leaf_map(CRMContact, contacts_data)
    organization_map = make_organization_map(
        organizations_data,
        user_map,
        industry_map,
        contacts_data,
        contact_map,
    )

    deal_products_map = make_deal_products_map(deals_data, product_map)
    tasks_by_deal_map = make_tasks_by_deal_map(tasks_data, user_map)

    return list(make_deal_map(
        deals_data,
        pipeline_stage_map,
        user_map,
        source_map,
        campaign_map,
        loss_reason_map,
        organization_map,
        contact_map,
        deal_products_map,
        tasks_by_deal_map,
    ).values())
