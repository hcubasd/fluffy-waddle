import psycopg


def delete_all(cur: psycopg.Cursor):
    for table in [
        "crm_tasks_users",
        "crm_teams_users",
        "crm_organizations_users",
        "crm_organizations_industries",
        "crm_deals_contacts",
        "crm_deals_products",
        "crm_tasks",
        "crm_deals",
        "crm_contacts",
        "crm_organizations",
        "crm_pipeline_stages",
        "crm_teams",
        "crm_pipelines",
        "crm_users",
        "crm_campaigns",
        "crm_sources",
        "crm_loss_reasons",
        "crm_products",
        "crm_industries",
    ]:
        cur.execute(f"DELETE FROM sales.{table}")
