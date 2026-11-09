# Reason Code

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlJlYXNvbkNvZGU


# Class Name

`ReasonCodeEnum`


# Fields

| Name |
|  --- |
| `ACTIONCLAIMFORBIDDEN` |
| `ASSURANCECLAIMFORBIDDEN` |
| `CITATIONUNKNOWN` |
| `CITATIONREGIONMISMATCH` |
| `CITATIONTHEMEMISMATCH` |
| `CLAIMREFERENCETYPEMISMATCH` |
| `FUTUREOBSERVATION` |
| `STALEOBSERVATION` |
| `DOCUMENTUPDATEINFUTURE` |
| `CURRENTPOLICYNOTESTABLISHED` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    reasonCode := models.ReasonCodeEnum_FUTUREOBSERVATION

}
```



