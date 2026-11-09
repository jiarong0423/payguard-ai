# Dispute Approval Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVBcHByb3ZhbFJlc3BvbnNl

DisputeApprovalResponse.


# Class Name

`DisputeApprovalResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Action` | `string` | Required, Constant | Action.<br><br>**Value**: `"review_draft"` |
| `AuthenticatedActor` | `string` | Required, Constant | Authenticated actor.<br><br>**Value**: `"False"` |
| `CaseRef` | `string` | Required | Case ref. |
| `DurableApproval` | `string` | Required, Constant | Durable approval.<br><br>**Value**: `"False"` |
| `ExternalSubmission` | `string` | Required, Constant | External submission.<br><br>**Value**: `"FROZEN"` |
| `Retention` | `string` | Required, Constant | Retention.<br><br>**Value**: `"SESSION_MEMORY_ONLY"` |
| `ReviewedAt` | `DateTime` | Required | Reviewed at. |
| `Reviewer` | `string` | Required, Constant | Reviewer.<br><br>**Value**: `"DEMO_OPERATOR_UNAUTHENTICATED"` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"local_draft_reviewed"` |


# Example

```csharp
using System.Globalization;
using TradeGlotLocalConsole.Standard.Models;

DisputeApprovalResponse disputeApprovalResponse = new DisputeApprovalResponse
{
    Action = "review_draft",
    AuthenticatedActor = "False",
    CaseRef = "case_ref6",
    DurableApproval = "False",
    ExternalSubmission = "FROZEN",
    Retention = "SESSION_MEMORY_ONLY",
    ReviewedAt = DateTime.ParseExact("2016-03-13T12:52:32.123Z", "yyyy'-'MM'-'dd'T'HH':'mm':'ss.FFFFFFFK",
        provider: CultureInfo.InvariantCulture,
        DateTimeStyles.RoundtripKind),
    Reviewer = "DEMO_OPERATOR_UNAUTHENTICATED",
    Source = "synthetic",
    Status = "local_draft_reviewed",
};
```



