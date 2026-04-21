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
        +string pipeline_id
        +string description [0..1]
        +string objective [0..1]
        +int display_order
    }
    class CRMOrganization {
        +string owner_id [0..1]
        +string description [0..1]
        +string url [0..1]
        +dict address [0..1]
    }
    class CRMContact {
        +string organization_id [0..1]
        +string job_title [0..1]
        +list emails
        +list phones
        +list social_profiles
        +list legal_bases
    }

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
    CRMOrganization "0..*" o-- "0..*" CRMSegment : segments
    CRMOrganization "0..*" o-- "0..*" CRMUser : followers
```

Each class only shows fields it adds over its parent. Omitted multiplicity means `[1..1]`.
