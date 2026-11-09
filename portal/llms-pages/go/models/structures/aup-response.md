# Aup Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkF1cFJlc3BvbnNl

AupResponse.


# Class Name

`AupResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `ComplianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `DescriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `EvaluatedAt` | `string` | Required | Evaluated at. |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `ExpiresAt` | `string` | Required | Expires at. |
| `Findings` | [`[]models.Finding`](http://localhost:3000/llms-pages/go/models/structures/finding.md) | Required | Findings. |
| `MatchStatus` | [`models.MatchStatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/match-status.md) | Required | Match status. |
| `PolicyUrl` | `string` | Required, Constant | Policy url.<br><br>**Value**: `"https://www.paypal.com/us/legalhub/paypal/acceptableuse-full"` |
| `PolicyVersion` | `string` | Required | Policy version.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` |
| `Recommendation` | `string` | Required | Recommendation.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `WarningCopyVersion` | `string` | Required, Constant | Warning copy version.<br><br>**Value**: `"aup-warning-v1"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    aupResponse := models.AupResponse{
        AdvisoryOnly:               "True",
        ComplianceDecision:         "NOT_MADE",
        CurrentPolicyApplicability: "NOT_ESTABLISHED",
        DescriptionDigest:          "description_digest8",
        EvaluatedAt:                "evaluated_at4",
        EvaluationId:               "evaluation_id4",
        ExpiresAt:                  "expires_at4",
        Findings:                   []models.Finding{
            models.Finding{
                Category: models.CategoryEnum_WEAPONS,
                Code:     "keyword_requires_policy_review",
            },
        },
        MatchStatus:                models.MatchStatusEnum_NOMATCH,
        PolicyUrl:                  "https://www.paypal.com/us/legalhub/paypal/acceptableuse-full",
        PolicyVersion:              "policy_version8",
        Recommendation:             "recommendation6",
        Source:                     "synthetic",
        WarningCopyVersion:         "aup-warning-v1",
    }

}
```



