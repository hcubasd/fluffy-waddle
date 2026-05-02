import psycopg


def select_industries(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_industries")
    return cur.fetchall()

def select_products(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_products")
    return cur.fetchall()

def select_loss_reasons(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_loss_reasons")
    return cur.fetchall()

def select_sources(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_sources")
    return cur.fetchall()

def select_campaigns(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_campaigns")
    return cur.fetchall()

def select_teams(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_teams")
    return cur.fetchall()

def select_teams_users(cur: psycopg.Cursor):
    cur.execute("SELECT team_id, user_id FROM sales.crm_teams_users")
    return cur.fetchall()

def select_users(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_users")
    return cur.fetchall()

def select_pipelines(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_pipelines")
    return cur.fetchall()

def select_pipeline_stages(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_pipeline_stages")
    return cur.fetchall()

def select_organizations_industries(cur: psycopg.Cursor):
    cur.execute("SELECT organization_id, industry_id FROM sales.crm_organizations_industries")
    return cur.fetchall()

def select_organizations_users(cur: psycopg.Cursor):
    cur.execute("SELECT organization_id, user_id FROM sales.crm_organizations_users")
    return cur.fetchall()

def select_organizations(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_organizations")
    return cur.fetchall()

def select_contacts(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_contacts")
    return cur.fetchall()

def select_deals_contacts(cur: psycopg.Cursor):
    cur.execute("SELECT deal_id, contact_id FROM sales.crm_deals_contacts")
    return cur.fetchall()

def select_deals_products(cur: psycopg.Cursor):
    cur.execute("SELECT deal_id, product_id FROM sales.crm_deals_products")
    return cur.fetchall()

def select_tasks_users(cur: psycopg.Cursor):
    cur.execute("SELECT task_id, user_id FROM sales.crm_tasks_users")
    return cur.fetchall()

def select_tasks(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_tasks")
    return cur.fetchall()

def select_deals(cur: psycopg.Cursor):
    cur.execute("SELECT * FROM sales.crm_deals")
    return cur.fetchall()
