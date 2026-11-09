# Dispute Approval Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVBcHByb3ZhbFJlc3BvbnNl

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
| `ReviewedAt` | `time.Time` | Required | Reviewed at. |
| `Reviewer` | `string` | Required, Constant | Reviewer.<br><br>**Value**: `"DEMO_OPERATOR_UNAUTHENTICATED"` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"local_draft_reviewed"` |


# Example

```go
package main

import (
    "log"
    "time"
    "tradeglotlocalconsole/models"
)

func main() {
    parseTime := func(layout, value string, errCallback func(error)) time.Time {
        dateTime, err := time.Parse(layout, value)
        if err != nil {
            errCallback(err) 
       }
        return dateTime
    }
    disputeApprovalResponse := models.DisputeApprovalResponse{
        Action:             "review_draft",
        AuthenticatedActor: "False",
        CaseRef:            "case_ref6",
        DurableApproval:    "False",
        ExternalSubmission: "FROZEN",
        Retention:          "SESSION_MEMORY_ONLY",
        ReviewedAt:         parseTime(time.RFC3339, "2016-03-13T12:52:32.123Z", func(err error) { log.Fatalln(err) }),
        Reviewer:           "DEMO_OPERATOR_UNAUTHENTICATED",
        Source:             "synthetic",
        Status:             "local_draft_reviewed",
    }

}
```



