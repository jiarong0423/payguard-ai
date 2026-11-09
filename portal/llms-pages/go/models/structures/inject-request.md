# Inject Request

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Class Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Scenario` | [`models.Scenario5Enum`](http://localhost:3000/llms-pages/go/models/enumerations/scenario-5.md) | Required | Scenario. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    injectRequest := models.InjectRequest{
        Scenario: models.Scenario5Enum_BURST,
    }

}
```



