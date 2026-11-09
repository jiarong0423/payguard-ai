# Send Refusal

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlNlbmRSZWZ1c2Fs


# Class Name

`SendRefusalEnum`


# Fields

| Name |
|  --- |
| `ACCOUNTIDENTITYUNKNOWN` |
| `DISPUTENOTTHISACCOUNT` |
| `DISPUTEDETAILREQUIRED` |
| `SELLEREVIDENCEALREADYSUBMITTED` |
| `DISPUTENOTAWAITINGSELLER` |
| `DISPUTEEVIDENCENOTOFFERED` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    sendRefusal := models.SendRefusalEnum_ACCOUNTIDENTITYUNKNOWN

}
```



