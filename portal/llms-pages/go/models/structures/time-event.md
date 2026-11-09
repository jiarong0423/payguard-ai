# Time Event

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlRpbWVFdmVudA

TimeEvent.


# Class Name

`TimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `At` | `string` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `Kind` | [`models.KindEnum`](http://localhost:3000/llms-pages/go/models/enumerations/kind.md) | Required | Kind. |
| `Source` | [`models.Source5Enum`](http://localhost:3000/llms-pages/go/models/enumerations/source-5.md) | Required | Source. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    timeEvent := models.TimeEvent{
        At:                   "at6",
        Kind:                 models.KindEnum_DELIVERY,
        Source:               models.Source5Enum_PROVIDER,
    }

}
```



