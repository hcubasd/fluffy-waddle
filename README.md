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

    CRMNamedModel --|> CRMModel
    CRMUser --|> CRMNamedModel
    CRMCampaign --|> CRMNamedModel
    CRMLostReason --|> CRMNamedModel
    CRMPipeline --|> CRMNamedModel
    CRMProduct --|> CRMNamedModel
    CRMSegment --|> CRMNamedModel
    CRMSource --|> CRMNamedModel
    CRMTeam --|> CRMNamedModel
```

Each class only shows fields it adds over its parent. Omitted multiplicity means `[1..1]`.
