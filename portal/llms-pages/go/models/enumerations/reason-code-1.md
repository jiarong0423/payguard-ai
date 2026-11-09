# Reason Code 1

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlJlYXNvbkNvZGUx


# Class Name

`ReasonCode1Enum`


# Fields

| Name |
|  --- |
| `SUMMARYCOVERAGEINCOMPLETE` |
| `CURRENTPOLICYAPPLICABILITYNOTESTABLISHED` |
| `FUTUREOBSERVATION` |
| `STALEOBSERVATION` |
| `DOCUMENTUPDATEDATEMISSING` |
| `DOCUMENTUPDATEINFUTURE` |
| `UNKNOWNEFFECTIVEDATE` |
| `EFFECTIVEDATEINFUTURE` |
| `APIREFERENCENOTPOLICY` |
| `PROCEDURENOTAPPLICABLEPOLICY` |
| `NOOFFICIALPOLICYCOVERAGE` |
| `NOREFERENCECOVERAGE` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    reasonCode1 := models.ReasonCode1Enum_NOOFFICIALPOLICYCOVERAGE

}
```



