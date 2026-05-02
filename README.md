# fluffy-waddle

Shared Pydantic data model for the **modest-galois** project. All Python workers (CRM sync, and future WMS, TMS, ERP integrations) import from this package.

This package stays intentionally **domain-first**: it models nested business objects, not database rows. Names track the database entities, but the public API is a graph of related classes with inheritance and aggregate roots.

## Sales class diagram

```mermaid
classDiagram
    class CRMModel {
        +string id
        +datetime created_at
        +datetime updated_at
    }
    class CRMNamedModel {
        +string name
    }
    class CRMUser {
        +string email [0..1]
        +string phone [0..1]
        +CRMTeam team [0..1]
    }
    class CRMCampaign {
        +string description [0..1]
    }
    class CRMLossReason
    class CRMPipeline {
        +int display_order
    }
    class CRMProduct {
        +Decimal price
        +string description [0..1]
    }
    class CRMIndustry
    class CRMSource {
        +string description [0..1]
    }
    class CRMTeam
    class CRMPipelineStage {
        +string description [0..1]
        +string objective [0..1]
        +int display_order
    }
    class CRMOrganization {
        +string description [0..1]
        +string url [0..1]
        +dict address [0..1]
    }
    class CRMContact {
        +string job_title [0..1]
        +list emails
        +list phones
        +list social_profiles
    }
    class CRMDeal {
        +Decimal value [0..1]
        +date expected_close_date [0..1]
        +int rating [0..1]
        +string status
        +datetime closed_at [0..1]
    }
    class CRMTask {
        +string description [0..1]
        +string type
        +string status
        +datetime due_date [0..1]
        +datetime completed_at [0..1]
    }

    %% Inheritance
    CRMNamedModel --|> CRMModel
    CRMUser --|> CRMNamedModel
    CRMCampaign --|> CRMNamedModel
    CRMLossReason --|> CRMNamedModel
    CRMPipeline --|> CRMNamedModel
    CRMProduct --|> CRMNamedModel
    CRMIndustry --|> CRMNamedModel
    CRMSource --|> CRMNamedModel
    CRMTeam --|> CRMNamedModel
    CRMPipelineStage --|> CRMNamedModel
    CRMOrganization --|> CRMNamedModel
    CRMContact --|> CRMNamedModel
    CRMDeal --|> CRMNamedModel
    CRMTask --|> CRMNamedModel

    %% Associations
    CRMPipelineStage "0..*" --> "1" CRMPipeline : pipeline
    CRMOrganization "0..*" --> "0..1" CRMUser : owner
    CRMOrganization "0..*" o-- "0..*" CRMIndustry : industries
    CRMOrganization "0..*" o-- "0..*" CRMUser : followers
    CRMOrganization "1" *-- "0..*" CRMContact : contacts
    CRMDeal "0..*" --> "1" CRMPipelineStage : stage
    CRMDeal "0..*" --> "0..1" CRMUser : owner
    CRMDeal "0..*" --> "0..1" CRMSource : source
    CRMDeal "0..*" --> "0..1" CRMCampaign : campaign
    CRMDeal "0..*" --> "0..1" CRMLossReason : loss_reason
    CRMDeal "0..*" --> "0..1" CRMOrganization : organization
    CRMDeal "0..*" o-- "0..*" CRMContact : contacts
    CRMDeal "0..*" o-- "0..*" CRMProduct : products
    CRMDeal "1" *-- "0..*" CRMTask : tasks
    CRMTask "0..*" --> "1" CRMUser : created_by
    CRMTask "0..*" --> "0..1" CRMUser : completed_by
    CRMTask "0..*" o-- "0..*" CRMUser : assignees
    CRMUser "0..*" --> "0..1" CRMTeam : team
```

`CRMDeal` is the main aggregate root for the sales graph. Child objects nested under a deal (`tasks`) intentionally do **not** carry backreference IDs to the parent deal; workers should navigate outward from the deal graph instead.

## Testing

Tests validate the full insert/assemble roundtrip against a live Postgres database seeded with JSON fixtures.

Spin up the database and run migrations (uses `curly-spoon` to apply the full schema):

```bash
docker compose up -d
```

Then run pytest from inside the `app` container:

```bash
pytest tests/
```

The `app` service mounts the repo at `/root/app` and loads `.env` (Postgres connection vars) automatically.

### Test structure

```
tests/
  data/           # JSON fixture files (one per entity type)
  map_makers.py   # builds domain models from raw fixture data
  inserter.py     # writes domain models to the DB
  selector.py     # reads raw rows back from the DB
  assembler.py    # reassembles domain models from raw rows
  deals_repository.py  # aggregate read/write repository for the deals graph
  test_deals.py   # roundtrip: insert fixtures → fetch → assert equality
```

`CRMDeal` is the aggregate root tested here. The roundtrip covers the full sales graph: pipelines, stages, organizations, contacts, products, tasks, teams, users, and all bridge tables.

## Scripts

Helper scripts for setting up a development environment on a new machine:

- `scripts/config-helix.sh` — configures the Helix editor for this project's stack
- `scripts/install-requirements.sh` — installs Python dependencies and the package in editable mode
