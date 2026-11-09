# Dispute Approval Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVBcHByb3ZhbFJlc3BvbnNl

DisputeApprovalResponse.


# Class Name

`DisputeApprovalResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Action` | `String` | Required, Constant | Action.<br><br>**Value**: `"review_draft"` | String getAction() | setAction(String action) |
| `AuthenticatedActor` | `String` | Required, Constant | Authenticated actor.<br><br>**Value**: `"False"` | String getAuthenticatedActor() | setAuthenticatedActor(String authenticatedActor) |
| `CaseRef` | `String` | Required | Case ref. | String getCaseRef() | setCaseRef(String caseRef) |
| `DurableApproval` | `String` | Required, Constant | Durable approval.<br><br>**Value**: `"False"` | String getDurableApproval() | setDurableApproval(String durableApproval) |
| `ExternalSubmission` | `String` | Required, Constant | External submission.<br><br>**Value**: `"FROZEN"` | String getExternalSubmission() | setExternalSubmission(String externalSubmission) |
| `Retention` | `String` | Required, Constant | Retention.<br><br>**Value**: `"SESSION_MEMORY_ONLY"` | String getRetention() | setRetention(String retention) |
| `ReviewedAt` | `LocalDateTime` | Required | Reviewed at. | LocalDateTime getReviewedAt() | setReviewedAt(LocalDateTime reviewedAt) |
| `Reviewer` | `String` | Required, Constant | Reviewer.<br><br>**Value**: `"DEMO_OPERATOR_UNAUTHENTICATED"` | String getReviewer() | setReviewer(String reviewer) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |
| `Status` | `String` | Required, Constant | Status.<br><br>**Value**: `"local_draft_reviewed"` | String getStatus() | setStatus(String status) |


# Example

```java
import m18000.m0.m0.m127.DateTimeHelper;
import m18000.m0.m0.m127.models.DisputeApprovalResponse;

DisputeApprovalResponse disputeApprovalResponse = new DisputeApprovalResponse.Builder(
    "review_draft",
    "False",
    "case_ref6",
    "False",
    "FROZEN",
    "SESSION_MEMORY_ONLY",
    DateTimeHelper.fromRfc8601DateTime("2016-03-13T12:52:32.123Z"),
    "DEMO_OPERATOR_UNAUTHENTICATED",
    "synthetic",
    "local_draft_reviewed"
)
.build();
```



