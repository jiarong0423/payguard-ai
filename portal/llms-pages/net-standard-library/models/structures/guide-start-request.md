# Guide Start Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Class Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `GoodsType` | [`GuideStartRequestGoodsType`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-start-request-goods-type.md) | Optional | This is a container for any-of cases. |
| `Scenario` | [`Scenario2Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/scenario-2.md) | Required | Scenario. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

GuideStartRequest guideStartRequest = new GuideStartRequest
{
    Scenario = Scenario2Enum.Velocity,
    GoodsType = GuideStartRequestGoodsType.FromGoodsType(GoodsTypeEnum.Physical),
};
```



