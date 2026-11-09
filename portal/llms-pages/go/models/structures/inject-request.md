# Inject Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Class Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Scenario` | [`models.Scenario5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/scenario-5.md) | Required | Scenario. |


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



