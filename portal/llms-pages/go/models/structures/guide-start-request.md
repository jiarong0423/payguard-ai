# Guide Start Request

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Class Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `GoodsType` | [`*models.GuideStartRequestGoodsType`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-start-request-goods-type.md) | Optional | This is a container for any-of cases. |
| `Scenario` | [`models.Scenario2Enum`](http://localhost:3000/llms-pages/go/models/enumerations/scenario-2.md) | Required | Scenario. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideStartRequest := models.GuideStartRequest{
        GoodsType: models.ToPointer(models.GuideStartRequestGoodsTypeContainer.FromGoodsType(models.GoodsTypeEnum_PHYSICAL)),
        Scenario:  models.Scenario2Enum_VELOCITY,
    }

}
```



