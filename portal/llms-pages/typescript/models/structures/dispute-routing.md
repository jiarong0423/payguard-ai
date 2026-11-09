# Dispute Routing

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVSb3V0aW5n

DisputeRouting.


# Interface Name

`DisputeRouting`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `availableActions` | `string[]` | Required | Available actions.<br><br>**Constraints**: *Maximum Items*: `20` |
| `disputeLifeCycleStage` | [`DisputeLifeCycleStageEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `dueState` | [`DueStateEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/due-state.md) | Required | Due state. |
| `humanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `'True'` |
| `overallState` | [`OverallStateEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/overall-state.md) | Required | Overall state. |
| `providerSubmission` | `string` | Required, Constant | Provider submission.<br><br>**Value**: `'NOT_PERFORMED'` |
| `reason` | [`Reason2Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/reason-2.md) | Required | Reason. |
| `requirements` | [`DisputeRequirement[]`](http://localhost:3000/llms-pages/typescript/models/structures/dispute-requirement.md) | Required | Requirements.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `schemaVersion` | `number` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `sellerResponseDueDate` | `string` | Required | Seller response due date.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `snapshotClass` | `string` | Required, Constant | Snapshot class.<br><br>**Value**: `'SYNTHETIC_PROVIDER_FIXTURE'` |
| `status` | [`Status3Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-3.md) | Required | Status. |


# Example

```ts
import {
  DisputeLifeCycleStageEnum,
  DisputeRouting,
  DueStateEnum,
  OverallStateEnum,
  Reason2Enum,
  RequirementStateEnum,
  Status3Enum,
} from 'tradeglot-local-consolelib';

const disputeRouting: DisputeRouting = {
  availableActions: [
    'available_actions4',
    'available_actions5'
  ],
  disputeLifeCycleStage: DisputeLifeCycleStageEnum.ARBITRATION,
  dueState: DueStateEnum.OPEN,
  humanReviewRequired: 'True',
  overallState: OverallStateEnum.DUEDATEEXPIRED,
  providerSubmission: 'NOT_PERFORMED',
  reason: Reason2Enum.UNAUTHORISED,
  requirements: [
    {
      acceptedAttachmentCount: 20,
      mandatory: false,
      proofCount: 60,
      providerEvidenceType: 'provider_evidence_type0',
      requestId: 'request_id8',
      requirementState: RequirementStateEnum.CONTEXTONLY,
      source: 'source2',
      action: 'String5',
      evidenceType: 'String3',
    }
  ],
  schemaVersion: 1,
  sellerResponseDueDate: 'seller_response_due_date2',
  snapshotClass: 'SYNTHETIC_PROVIDER_FIXTURE',
  status: Status3Enum.WAITINGFORSELLERRESPONSE,
};
```



