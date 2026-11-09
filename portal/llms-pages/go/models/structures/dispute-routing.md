# Dispute Routing

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVSb3V0aW5n

DisputeRouting.


# Class Name

`DisputeRouting`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AvailableActions` | `[]string` | Required | Available actions.<br><br>**Constraints**: *Maximum Items*: `20` |
| `DisputeLifeCycleStage` | [`models.DisputeLifeCycleStageEnum`](http://localhost:3000/llms-pages/go/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `DueState` | [`models.DueStateEnum`](http://localhost:3000/llms-pages/go/models/enumerations/due-state.md) | Required | Due state. |
| `HumanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `OverallState` | [`models.OverallStateEnum`](http://localhost:3000/llms-pages/go/models/enumerations/overall-state.md) | Required | Overall state. |
| `ProviderSubmission` | `string` | Required, Constant | Provider submission.<br><br>**Value**: `"NOT_PERFORMED"` |
| `Reason` | [`models.Reason2Enum`](http://localhost:3000/llms-pages/go/models/enumerations/reason-2.md) | Required | Reason. |
| `Requirements` | [`[]models.DisputeRequirement`](http://localhost:3000/llms-pages/go/models/structures/dispute-requirement.md) | Required | Requirements.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `SellerResponseDueDate` | `string` | Required | Seller response due date.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `SnapshotClass` | `string` | Required, Constant | Snapshot class.<br><br>**Value**: `"SYNTHETIC_PROVIDER_FIXTURE"` |
| `Status` | [`models.Status3Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-3.md) | Required | Status. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    disputeRouting := models.DisputeRouting{
        AvailableActions:      []string{
            "available_actions4",
            "available_actions5",
        },
        DisputeLifeCycleStage: models.DisputeLifeCycleStageEnum_ARBITRATION,
        DueState:              models.DueStateEnum_OPEN,
        HumanReviewRequired:   "True",
        OverallState:          models.OverallStateEnum_DUEDATEEXPIRED,
        ProviderSubmission:    "NOT_PERFORMED",
        Reason:                models.Reason2Enum_UNAUTHORISED,
        Requirements:          []models.DisputeRequirement{
            models.DisputeRequirement{
                AcceptedAttachmentCount: 20,
                Action:                  models.ToPointer(models.DisputeRequirementActionContainer.FromString("String5")),
                EvidenceType:            models.ToPointer(models.DisputeRequirementEvidenceTypeContainer.FromString("String3")),
                Mandatory:               false,
                ProofCount:              60,
                ProviderEvidenceType:    "provider_evidence_type0",
                RequestId:               "request_id8",
                RequirementState:        models.RequirementStateEnum_CONTEXTONLY,
                Source:                  "source2",
            },
        },
        SchemaVersion:         1,
        SellerResponseDueDate: "seller_response_due_date2",
        SnapshotClass:         "SYNTHETIC_PROVIDER_FIXTURE",
        Status:                models.Status3Enum_WAITINGFORSELLERRESPONSE,
    }

}
```



