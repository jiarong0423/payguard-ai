# Advisory Claim Gate

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkFkdmlzb3J5Q2xhaW1HYXRl

AdvisoryClaimGate.


# Class Name

`AdvisoryClaimGate`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ClaimIndex` | `int` | Required | Claim index.<br><br>**Constraints**: `>= 0`, `<= 19` |
| `ClaimType` | [`models.ClaimTypeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/claim-type.md) | Required | Claim type. |
| `ReasonCodes` | [`[]models.ReasonCodeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/reason-code.md) | Required | Reason codes.<br><br>**Constraints**: *Maximum Items*: `10` |
| `Status` | [`models.StatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/status.md) | Required | Status. |
| `TrustedCitationChunkIds` | `[]string` | Required | Trusted citation chunk ids.<br><br>**Constraints**: *Maximum Items*: `10`, *Pattern*: `^[A-Z0-9-]{1,128}$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    advisoryClaimGate := models.AdvisoryClaimGate{
        ClaimIndex:              19,
        ClaimType:               models.ClaimTypeEnum_FINANCIALACTION,
        ReasonCodes:             []models.ReasonCodeEnum{
            models.ReasonCodeEnum_CLAIMREFERENCETYPEMISMATCH,
            models.ReasonCodeEnum_CITATIONTHEMEMISMATCH,
            models.ReasonCodeEnum_CITATIONREGIONMISMATCH,
        },
        Status:                  models.StatusEnum_STRUCTURECOMPATIBLE,
        TrustedCitationChunkIds: []string{
            "trusted_citation_chunk_ids6",
            "trusted_citation_chunk_ids7",
            "trusted_citation_chunk_ids8",
        },
    }

}
```



