# Dispute Approval Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVBcHByb3ZhbFJlc3BvbnNl

DisputeApprovalResponse.


# Interface Name

`DisputeApprovalResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | `string` | Required, Constant | Action.<br><br>**Value**: `'review_draft'` |
| `authenticatedActor` | `string` | Required, Constant | Authenticated actor.<br><br>**Value**: `'False'` |
| `caseRef` | `string` | Required | Case ref. |
| `durableApproval` | `string` | Required, Constant | Durable approval.<br><br>**Value**: `'False'` |
| `externalSubmission` | `string` | Required, Constant | External submission.<br><br>**Value**: `'FROZEN'` |
| `retention` | `string` | Required, Constant | Retention.<br><br>**Value**: `'SESSION_MEMORY_ONLY'` |
| `reviewedAt` | `string` | Required | Reviewed at. |
| `reviewer` | `string` | Required, Constant | Reviewer.<br><br>**Value**: `'DEMO_OPERATOR_UNAUTHENTICATED'` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'local_draft_reviewed'` |


# Example

```ts
import { DisputeApprovalResponse } from 'tradeglot-local-consolelib';

const disputeApprovalResponse: DisputeApprovalResponse = {
  action: 'review_draft',
  authenticatedActor: 'False',
  caseRef: 'case_ref6',
  durableApproval: 'False',
  externalSubmission: 'FROZEN',
  retention: 'SESSION_MEMORY_ONLY',
  reviewedAt: '2016-03-13T12:52:32.123Z',
  reviewer: 'DEMO_OPERATOR_UNAUTHENTICATED',
  source: 'synthetic',
  status: 'local_draft_reviewed',
};
```



