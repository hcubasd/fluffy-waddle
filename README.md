# fluffy-waddle

Shared Pydantic data model for the **modest-galois** project. All Python workers (CRM sync, and future WMS, TMS, ERP integrations) import from this package.

## Class diagram

```mermaid
classDiagram
    class CRMModel {
        +string id
        +datetime created_at
        +datetime updated_at
    }
    class CRMNamedModel {
        +string name [0..1]
    }
    class CRMUser {
        +string email [0..1]
        +string phone [0..1]
    }
    class CRMCampaign {
        +string description [0..1]
    }
    class CRMLostReason
    class CRMPipeline {
        +int display_order
    }
    class CRMProduct {
        +Decimal price
        +bool visible
        +string description [0..1]
    }
    class CRMSegment
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
        +list legal_bases
    }
    class CRMDeal {
        +Decimal recurrence_price
        +Decimal one_time_price
        +Decimal total_price
        +date expected_close_date [0..1]
        +int rating [0..1]
        +string status
        +datetime closed_at [0..1]
        +dict distribution_settings [0..1]
    }
    class CRMDealProduct {
        +string deal_id
        +Decimal price
        +Decimal quantity
        +string discount_type [0..1]
        +Decimal discount
        +Decimal total_price
        +string billing_frequency [0..1]
    }
    class CRMDealNote {
        +string id
        +string deal_id
        +string description
        +datetime created_at
        +datetime pinned_at [0..1]
        +datetime edited_at [0..1]
    }
    class CRMTask {
        +string deal_id [0..1]
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
    CRMLostReason --|> CRMNamedModel
    CRMPipeline --|> CRMNamedModel
    CRMProduct --|> CRMNamedModel
    CRMSegment --|> CRMNamedModel
    CRMSource --|> CRMNamedModel
    CRMTeam --|> CRMNamedModel
    CRMPipelineStage --|> CRMNamedModel
    CRMOrganization --|> CRMNamedModel
    CRMContact --|> CRMNamedModel
    CRMDeal --|> CRMNamedModel
    CRMDealProduct --|> CRMModel
    CRMTask --|> CRMNamedModel

    %% Associations
    CRMPipelineStage "0..*" --> "1" CRMPipeline : pipeline
    CRMOrganization "0..*" --> "0..1" CRMUser : owner
    CRMOrganization "0..*" o-- "0..*" CRMSegment : segments
    CRMOrganization "0..*" o-- "0..*" CRMUser : followers
    CRMContact "0..*" --> "0..1" CRMOrganization : organization
    CRMDeal "0..*" --> "1" CRMPipelineStage : stage
    CRMDeal "0..*" --> "0..1" CRMUser : owner
    CRMDeal "0..*" --> "0..1" CRMSource : source
    CRMDeal "0..*" --> "0..1" CRMCampaign : campaign
    CRMDeal "0..*" --> "0..1" CRMLostReason : lost_reason
    CRMDeal "0..*" --> "0..1" CRMOrganization : organization
    CRMDeal "0..*" o-- "0..*" CRMContact : contacts
    CRMDeal "1" *-- "0..*" CRMDealProduct : products
    CRMDeal "1" *-- "0..*" CRMDealNote : notes
    CRMDealProduct "0..*" --> "1" CRMProduct : product
    CRMDealNote "0..*" --> "1" CRMUser : author
    CRMDealNote "0..*" --> "0..1" CRMUser : edited_by
    CRMDeal "1" *-- "0..*" CRMTask : tasks
    CRMTask "0..*" --> "1" CRMUser : created_by
    CRMTask "0..*" --> "0..1" CRMUser : completed_by
    CRMTask "0..*" o-- "0..*" CRMUser : owners
    CRMTeam "0..*" o-- "0..*" CRMUser : members
```

Each class only shows fields it adds over its parent. Omitted multiplicity means `[1..1]`. `CRMDealNote` inherits from Pydantic's `BaseModel` directly (not `CRMModel`) because the `deal_notes` table has no `updated_at` column. `CRMTask.deal_id` and `SyncCursor.connection_id` are kept as strings to avoid circular imports — navigate those relationships from the parent side.

## Integrations class diagram

```mermaid
classDiagram
    class IntegrationModel {
        +datetime created_at
        +datetime updated_at
    }
    class Connection {
        +string id
        +string provider
        +string account_name
        +string status
        +string client_id [0..1]
        +string client_secret [0..1]
        +string access_token [0..1]
        +string refresh_token [0..1]
        +string token_type [0..1]
        +datetime expires_at [0..1]
        +bool reauth_required
        +string redirect_uri [0..1]
        +dict config
        +datetime last_refresh_at [0..1]
        +string last_refresh_error [0..1]
    }
    class SyncCursor {
        +int id
        +string connection_id
        +string resource
        +string cursor_type
        +dict cursor
        +datetime last_sync_at [0..1]
        +string last_sync_status [0..1]
        +string last_error [0..1]
    }

    Connection --|> IntegrationModel
    SyncCursor --|> IntegrationModel
    Connection "1" *-- "0..*" SyncCursor : sync_cursors
```

> **Tip:** GitHub renders this with dagre and the layout gets crowded. For a clearer view, paste the diagram into the Mermaid Live Editor and switch the layout to ELK.
