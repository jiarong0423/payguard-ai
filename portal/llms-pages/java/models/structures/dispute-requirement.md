# Dispute Requirement

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVSZXF1aXJlbWVudA

DisputeRequirement.


# Class Name

`DisputeRequirement`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AcceptedAttachmentCount` | `int` | Required | Accepted attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` | int getAcceptedAttachmentCount() | setAcceptedAttachmentCount(int acceptedAttachmentCount) |
| `Action` | [`DisputeRequirementAction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/dispute-requirement-action.md) | Optional | This is a container for any-of cases. | DisputeRequirementAction getAction() | setAction(DisputeRequirementAction action) |
| `EvidenceType` | [`DisputeRequirementEvidenceType`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/dispute-requirement-evidence-type.md) | Optional | This is a container for any-of cases. | DisputeRequirementEvidenceType getEvidenceType() | setEvidenceType(DisputeRequirementEvidenceType evidenceType) |
| `Mandatory` | `boolean` | Required | Mandatory. | boolean getMandatory() | setMandatory(boolean mandatory) |
| `ProofCount` | `int` | Required | Proof count.<br><br>**Constraints**: `>= 0`, `<= 128` | int getProofCount() | setProofCount(int proofCount) |
| `ProviderEvidenceType` | `String` | Required | Provider evidence type.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` | String getProviderEvidenceType() | setProviderEvidenceType(String providerEvidenceType) |
| `RequestId` | `String` | Required | Request id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$` | String getRequestId() | setRequestId(String requestId) |
| `RequirementState` | [`RequirementStateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/requirement-state.md) | Required | Requirement state. | RequirementStateEnum getRequirementState() | setRequirementState(RequirementStateEnum requirementState) |
| `Source` | `String` | Required | Source.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` | String getSource() | setSource(String source) |


# Example

```java
import m18000.m0.m0.m127.models.DisputeRequirement;
import m18000.m0.m0.m127.models.RequirementStateEnum;
import m18000.m0.m0.m127.models.containers.DisputeRequirementAction;
import m18000.m0.m0.m127.models.containers.DisputeRequirementEvidenceType;

DisputeRequirement disputeRequirement = new DisputeRequirement.Builder(
    8,
    false,
    128,
    "provider_evidence_type4",
    "request_id6",
    RequirementStateEnum.CONTEXT_ONLY,
    "source2"
)
.action(DisputeRequirementAction.fromString(
        "String1"
    ))
.evidenceType(DisputeRequirementEvidenceType.fromString(
        "String3"
    ))
.build();
```



