# Dispute Approval Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVBcHByb3ZhbFJlc3BvbnNl

DisputeApprovalResponse.


# Class Name

`DisputeApprovalResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `action` | `string` | Required, Constant | Action.<br><br>**Value**: `'review_draft'` | getAction(): string | setAction(string action): void |
| `authenticatedActor` | `string` | Required, Constant | Authenticated actor.<br><br>**Value**: `'False'` | getAuthenticatedActor(): string | setAuthenticatedActor(string authenticatedActor): void |
| `caseRef` | `string` | Required | Case ref. | getCaseRef(): string | setCaseRef(string caseRef): void |
| `durableApproval` | `string` | Required, Constant | Durable approval.<br><br>**Value**: `'False'` | getDurableApproval(): string | setDurableApproval(string durableApproval): void |
| `externalSubmission` | `string` | Required, Constant | External submission.<br><br>**Value**: `'FROZEN'` | getExternalSubmission(): string | setExternalSubmission(string externalSubmission): void |
| `retention` | `string` | Required, Constant | Retention.<br><br>**Value**: `'SESSION_MEMORY_ONLY'` | getRetention(): string | setRetention(string retention): void |
| `reviewedAt` | `DateTime` | Required | Reviewed at. | getReviewedAt(): \DateTime | setReviewedAt(\DateTime reviewedAt): void |
| `reviewer` | `string` | Required, Constant | Reviewer.<br><br>**Value**: `'DEMO_OPERATOR_UNAUTHENTICATED'` | getReviewer(): string | setReviewer(string reviewer): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'local_draft_reviewed'` | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeApprovalResponseBuilder;
use TradeGlotLocalConsoleLib\Utils\DateTimeHelper;

$disputeApprovalResponse = DisputeApprovalResponseBuilder::init(
    'case_ref6',
    DateTimeHelper::fromRfc3339DateTimeRequired('2016-03-13T12:52:32.123Z')
)->build();
```



