# Aup Acknowledge Request

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVxdWVzdA

AupAcknowledgeRequest.


# Class Name

`AupAcknowledgeRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Choice` | [`models.ChoiceEnum`](http://localhost:3000/llms-pages/go/models/enumerations/choice.md) | Required | Choice. |
| `DescriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    aupAcknowledgeRequest := models.AupAcknowledgeRequest{
        Choice:            models.ChoiceEnum_ACKNOWLEDGEANDCONTINUE,
        DescriptionDigest: "description_digest0",
        EvaluationId:      "evaluation_id6",
    }

}
```



