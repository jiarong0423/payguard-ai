# Guide Start Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Class Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `GoodsType` | [`GuideStartRequestGoodsType`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-start-request-goods-type.md) | Optional | This is a container for any-of cases. |
| `Scenario` | [`Scenario2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/scenario-2.md) | Required | Scenario. |


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



