# Aup Acknowledge Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVzcG9uc2U

AupAcknowledgeResponse.


# Class Name

`AupAcknowledgeResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AcknowledgementToken` | [`models.AupAcknowledgeResponseAcknowledgementToken`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/aup-acknowledge-response-acknowledgement-token.md) | Required | This is a container for any-of cases. |
| `Choice` | [`models.ChoiceEnum`](http://localhost:3000/llms-pages/go/models/enumerations/choice.md) | Required | Choice. |
| `ComplianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` |
| `DescriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `ExpiresAt` | [`models.AupAcknowledgeResponseExpiresAt`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/aup-acknowledge-response-expires-at.md) | Required | This is a container for any-of cases. |
| `ExternalActionAuthorized` | `string` | Required, Constant | External action authorized.<br><br>**Value**: `"False"` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `WarningCopyVersion` | `string` | Required, Constant | Warning copy version.<br><br>**Value**: `"aup-warning-v1"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    aupAcknowledgeResponse := models.AupAcknowledgeResponse{
        AcknowledgementToken:     models.AupAcknowledgeResponseAcknowledgementTokenContainer.FromString("String9"),
        Choice:                   models.ChoiceEnum_ACKNOWLEDGEANDCONTINUE,
        ComplianceDecision:       "NOT_MADE",
        DescriptionDigest:        "description_digest6",
        EvaluationId:             "evaluation_id2",
        ExpiresAt:                models.AupAcknowledgeResponseExpiresAtContainer.FromString("String9"),
        ExternalActionAuthorized: "False",
        Source:                   "synthetic",
        WarningCopyVersion:       "aup-warning-v1",
    }

}
```



