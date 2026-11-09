# Dispute Routing

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVSb3V0aW5n

DisputeRouting.


# Class Name

`DisputeRouting`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AvailableActions` | `List<string>` | Required | Available actions.<br><br>**Constraints**: *Maximum Items*: `20` |
| `DisputeLifeCycleStage` | [`DisputeLifeCycleStageEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `DueState` | [`DueStateEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/due-state.md) | Required | Due state. |
| `HumanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `OverallState` | [`OverallStateEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/overall-state.md) | Required | Overall state. |
| `ProviderSubmission` | `string` | Required, Constant | Provider submission.<br><br>**Value**: `"NOT_PERFORMED"` |
| `Reason` | [`Reason2Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/reason-2.md) | Required | Reason. |
| `Requirements` | [`List<DisputeRequirement>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/dispute-requirement.md) | Required | Requirements.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `SellerResponseDueDate` | `string` | Required | Seller response due date.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `SnapshotClass` | `string` | Required, Constant | Snapshot class.<br><br>**Value**: `"SYNTHETIC_PROVIDER_FIXTURE"` |
| `Status` | [`Status3Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/status-3.md) | Required | Status. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

DisputeRouting disputeRouting = new DisputeRouting
{
    AvailableActions = new List<string>
    {
        "available_actions4",
        "available_actions5",
    },
    DisputeLifeCycleStage = DisputeLifeCycleStageEnum.ARBITRATION,
    DueState = DueStateEnum.OPEN,
    HumanReviewRequired = "True",
    OverallState = OverallStateEnum.DUEDATEEXPIRED,
    ProviderSubmission = "NOT_PERFORMED",
    Reason = Reason2Enum.UNAUTHORISED,
    Requirements = new List<DisputeRequirement>
    {
        new DisputeRequirement
        {
            AcceptedAttachmentCount = 20,
            Mandatory = false,
            ProofCount = 60,
            ProviderEvidenceType = "provider_evidence_type0",
            RequestId = "request_id8",
            RequirementState = RequirementStateEnum.CONTEXTONLY,
            Source = "source2",
            Action = DisputeRequirementAction.FromString("String5"),
            EvidenceType = DisputeRequirementEvidenceType.FromString("String3"),
        },
    },
    SchemaVersion = 1,
    SellerResponseDueDate = "seller_response_due_date2",
    SnapshotClass = "SYNTHETIC_PROVIDER_FIXTURE",
    Status = Status3Enum.WAITINGFORSELLERRESPONSE,
};
```



