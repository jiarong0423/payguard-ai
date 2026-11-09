# Advisory Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkFkdmlzb3J5UmVxdWVzdA

AdvisoryRequest.


# Class Name

`AdvisoryRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AsOf` | `string` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `CandidateJson` | `string` | Required | Candidate json.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8192` |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `ObservationMaxAgeDays` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `Theme` | [`models.ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/theme.md) | Required | Theme. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    advisoryRequest := models.AdvisoryRequest{
        AsOf:                  "as_of2",
        CandidateJson:         "candidate_json2",
        Jurisdiction:          "US",
        ObservationMaxAgeDays: 220,
        Theme:                 models.ThemeEnum_VELOCITYGUARD,
    }

}
```



