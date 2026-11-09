# Dispute Requirement

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVSZXF1aXJlbWVudA

DisputeRequirement.


# Interface Name

`DisputeRequirement`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `acceptedAttachmentCount` | `number` | Required | Accepted attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` |
| `action` | [`DisputeRequirementAction \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-requirement-action.md) | Optional | This is a container for any-of cases. |
| `evidenceType` | [`DisputeRequirementEvidenceType \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-requirement-evidence-type.md) | Optional | This is a container for any-of cases. |
| `mandatory` | `boolean` | Required | Mandatory. |
| `proofCount` | `number` | Required | Proof count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `providerEvidenceType` | `string` | Required | Provider evidence type.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` |
| `requestId` | `string` | Required | Request id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$` |
| `requirementState` | [`RequirementStateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/requirement-state.md) | Required | Requirement state. |
| `source` | `string` | Required | Source.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` |


# Example

```ts
import {
  DisputeRequirement,
  RequirementStateEnum,
} from 'tradeglot-local-consolelib';

const disputeRequirement: DisputeRequirement = {
  acceptedAttachmentCount: 8,
  mandatory: false,
  proofCount: 128,
  providerEvidenceType: 'provider_evidence_type4',
  requestId: 'request_id6',
  requirementState: RequirementStateEnum.CONTEXTONLY,
  source: 'source2',
  action: 'String1',
  evidenceType: 'String3',
};
```



