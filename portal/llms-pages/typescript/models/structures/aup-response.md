# Aup Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkF1cFJlc3BvbnNl

AupResponse.


# Interface Name

`AupResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `complianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `'NOT_MADE'` |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `descriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluatedAt` | `string` | Required | Evaluated at. |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `expiresAt` | `string` | Required | Expires at. |
| `findings` | [`Finding[]`](http://localhost:3000/llms-pages/typescript/models/structures/finding.md) | Required | Findings. |
| `matchStatus` | [`MatchStatusEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/match-status.md) | Required | Match status. |
| `policyUrl` | `string` | Required, Constant | Policy url.<br><br>**Value**: `'https://www.paypal.com/us/legalhub/paypal/acceptableuse-full'` |
| `policyVersion` | `string` | Required | Policy version.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` |
| `recommendation` | `string` | Required | Recommendation.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `warningCopyVersion` | `string` | Required, Constant | Warning copy version.<br><br>**Value**: `'aup-warning-v1'` |


# Example

```ts
import {
  AupResponse,
  CategoryEnum,
  MatchStatusEnum,
} from 'tradeglot-local-consolelib';

const aupResponse: AupResponse = {
  advisoryOnly: 'True',
  complianceDecision: 'NOT_MADE',
  currentPolicyApplicability: 'NOT_ESTABLISHED',
  descriptionDigest: 'description_digest8',
  evaluatedAt: 'evaluated_at4',
  evaluationId: 'evaluation_id4',
  expiresAt: 'expires_at4',
  findings: [
    {
      category: CategoryEnum.Weapons,
      code: 'keyword_requires_policy_review',
    }
  ],
  matchStatus: MatchStatusEnum.NOMATCH,
  policyUrl: 'https://www.paypal.com/us/legalhub/paypal/acceptableuse-full',
  policyVersion: 'policy_version8',
  recommendation: 'recommendation6',
  source: 'synthetic',
  warningCopyVersion: 'aup-warning-v1',
};
```



