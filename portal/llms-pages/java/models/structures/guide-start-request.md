# Guide Start Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Class Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `GoodsType` | [`GuideStartRequestGoodsType`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/guide-start-request-goods-type.md) | Optional | This is a container for any-of cases. | GuideStartRequestGoodsType getGoodsType() | setGoodsType(GuideStartRequestGoodsType goodsType) |
| `Scenario` | [`Scenario2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/scenario-2.md) | Required | Scenario. | Scenario2Enum getScenario() | setScenario(Scenario2Enum scenario) |


# Example

```java
import m18000.m0.m0.m127.models.GoodsTypeEnum;
import m18000.m0.m0.m127.models.GuideStartRequest;
import m18000.m0.m0.m127.models.Scenario2Enum;
import m18000.m0.m0.m127.models.containers.GuideStartRequestGoodsType;

GuideStartRequest guideStartRequest = new GuideStartRequest.Builder(
    Scenario2Enum.VELOCITY
)
.goodsType(GuideStartRequestGoodsType.fromGoodsType(
        GoodsTypeEnum.PHYSICAL
    ))
.build();
```



