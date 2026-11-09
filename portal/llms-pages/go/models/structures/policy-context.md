# Policy Context

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlBvbGljeUNvbnRleHQ

PolicyContext.


# Class Name

`PolicyContext`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AsOf` | `string` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
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
    policyContext := models.PolicyContext{
        AsOf:                  "as_of4",
        Jurisdiction:          "US",
        ObservationMaxAgeDays: 12,
        Theme:                 models.ThemeEnum_VELOCITYGUARD,
    }

}
```



