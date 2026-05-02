import psycopg
import json
from pathlib import Path

from deals_repository import DealsRepository
from map_makers import make_deals

DATA_DIR = Path(__file__).parent / "data"

def load(filename):
    with (DATA_DIR / filename).open() as f:
        return json.load(f)

deals = make_deals(
    campaigns_data=load("campaigns.json"),
    contacts_data=load("contacts.json"),
    deals_data=load("deals.json"),
    industries_data=load("industries.json"),
    loss_reasons_data=load("loss_reasons.json"),
    organizations_data=load("organizations.json"),
    pipeline_stages_data=load("pipeline_stages.json"),
    pipelines_data=load("pipelines.json"),
    products_data=load("products.json"),
    sources_data=load("sources.json"),
    tasks_data=load("tasks.json"),
    teams_data=load("teams.json"),
    users_data=load("users.json"),
)

def test_deals_roundtrip():
    conn = psycopg.connect()
    repo = DealsRepository(conn)
    repo.add_deals(deals)
    fetched = repo.get_deals()

    original = sorted([d.model_dump() for d in deals], key=lambda x: x["id"])
    retrieved = sorted([d.model_dump() for d in fetched], key=lambda x: x["id"])

    assert original == retrieved
    conn.close()
