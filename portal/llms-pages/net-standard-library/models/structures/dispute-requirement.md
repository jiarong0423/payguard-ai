# Dispute Requirement

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVSZXF1aXJlbWVudA

DisputeRequirement.


# Class Name

`DisputeRequirement`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AcceptedAttachmentCount` | `int` | Required | Accepted attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` |
| `Action` | [`DisputeRequirementAction`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-requirement-action.md) | Optional | This is a container for any-of cases. |
| `EvidenceType` | [`DisputeRequirementEvidenceType`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-requirement-evidence-type.md) | Optional | This is a container for any-of cases. |
| `Mandatory` | `bool` | Required | Mandatory. |
| `ProofCount` | `int` | Required | Proof count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `ProviderEvidenceType` | `string` | Required | Provider evidence type.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` |
| `RequestId` | `string` | Required | Request id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$` |
| `RequirementState` | [`RequirementStateEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/requirement-state.md) | Required | Requirement state. |
| `Source` | `string` | Required | Source.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

DisputeRequirement disputeRequirement = new DisputeRequirement
{
    AcceptedAttachmentCount = 8,
    Mandatory = false,
    ProofCount = 128,
    ProviderEvidenceType = "provider_evidence_type4",
    RequestId = "request_id6",
    RequirementState = RequirementStateEnum.CONTEXTONLY,
    Source = "source2",
    Action = DisputeRequirementAction.FromString("String1"),
    EvidenceType = DisputeRequirementEvidenceType.FromString("String3"),
};
```



