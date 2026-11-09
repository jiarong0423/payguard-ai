# Dispute Routing

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVSb3V0aW5n

DisputeRouting.


# Class Name

`DisputeRouting`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AvailableActions` | `List<String>` | Required | Available actions.<br><br>**Constraints**: *Maximum Items*: `20` | List<String> getAvailableActions() | setAvailableActions(List<String> availableActions) |
| `DisputeLifeCycleStage` | [`DisputeLifeCycleStageEnum`](http://localhost:3000/llms-pages/java/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. | DisputeLifeCycleStageEnum getDisputeLifeCycleStage() | setDisputeLifeCycleStage(DisputeLifeCycleStageEnum disputeLifeCycleStage) |
| `DueState` | [`DueStateEnum`](http://localhost:3000/llms-pages/java/models/enumerations/due-state.md) | Required | Due state. | DueStateEnum getDueState() | setDueState(DueStateEnum dueState) |
| `HumanReviewRequired` | `String` | Required, Constant | Human review required.<br><br>**Value**: `"True"` | String getHumanReviewRequired() | setHumanReviewRequired(String humanReviewRequired) |
| `OverallState` | [`OverallStateEnum`](http://localhost:3000/llms-pages/java/models/enumerations/overall-state.md) | Required | Overall state. | OverallStateEnum getOverallState() | setOverallState(OverallStateEnum overallState) |
| `ProviderSubmission` | `String` | Required, Constant | Provider submission.<br><br>**Value**: `"NOT_PERFORMED"` | String getProviderSubmission() | setProviderSubmission(String providerSubmission) |
| `Reason` | [`Reason2Enum`](http://localhost:3000/llms-pages/java/models/enumerations/reason-2.md) | Required | Reason. | Reason2Enum getReason() | setReason(Reason2Enum reason) |
| `Requirements` | [`List<DisputeRequirement>`](http://localhost:3000/llms-pages/java/models/structures/dispute-requirement.md) | Required | Requirements.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` | List<DisputeRequirement> getRequirements() | setRequirements(List<DisputeRequirement> requirements) |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | int getSchemaVersion() | setSchemaVersion(int schemaVersion) |
| `SellerResponseDueDate` | `String` | Required | Seller response due date.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | String getSellerResponseDueDate() | setSellerResponseDueDate(String sellerResponseDueDate) |
| `SnapshotClass` | `String` | Required, Constant | Snapshot class.<br><br>**Value**: `"SYNTHETIC_PROVIDER_FIXTURE"` | String getSnapshotClass() | setSnapshotClass(String snapshotClass) |
| `Status` | [`Status3Enum`](http://localhost:3000/llms-pages/java/models/enumerations/status-3.md) | Required | Status. | Status3Enum getStatus() | setStatus(Status3Enum status) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.DisputeLifeCycleStageEnum;
import m18000.m0.m0.m127.models.DisputeRequirement;
import m18000.m0.m0.m127.models.DisputeRouting;
import m18000.m0.m0.m127.models.DueStateEnum;
import m18000.m0.m0.m127.models.OverallStateEnum;
import m18000.m0.m0.m127.models.Reason2Enum;
import m18000.m0.m0.m127.models.RequirementStateEnum;
import m18000.m0.m0.m127.models.Status3Enum;
import m18000.m0.m0.m127.models.containers.DisputeRequirementAction;
import m18000.m0.m0.m127.models.containers.DisputeRequirementEvidenceType;

DisputeRouting disputeRouting = new DisputeRouting.Builder(
    Arrays.asList(
        "available_actions4",
        "available_actions5"
    ),
    DisputeLifeCycleStageEnum.ARBITRATION,
    DueStateEnum.OPEN,
    "True",
    OverallStateEnum.DUE_DATE_EXPIRED,
    "NOT_PERFORMED",
    Reason2Enum.UNAUTHORISED,
    Arrays.asList(
        new DisputeRequirement.Builder(
            20,
            false,
            60,
            "provider_evidence_type0",
            "request_id8",
            RequirementStateEnum.CONTEXT_ONLY,
            "source2"
        )
        .action(DisputeRequirementAction.fromString(
                "String5"
            ))
        .evidenceType(DisputeRequirementEvidenceType.fromString(
                "String3"
            ))
        .build()
    ),
    1,
    "seller_response_due_date2",
    "SYNTHETIC_PROVIDER_FIXTURE",
    Status3Enum.WAITING_FOR_SELLER_RESPONSE
)
.build();
```



