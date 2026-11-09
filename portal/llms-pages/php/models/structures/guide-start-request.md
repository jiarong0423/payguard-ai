# Guide Start Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Class Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `goodsType` | string([GoodsTypeEnum](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/goods-type.md))\|null | Optional | This is a container for any-of cases. | getGoodsType(): ?string | setGoodsType(?string goodsType): void |
| `scenario` | [`string(Scenario2Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/scenario-2.md) | Required | Scenario. | getScenario(): string | setScenario(string scenario): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideStartRequestBuilder;
use TradeGlotLocalConsoleLib\Models\Scenario2Enum;
use TradeGlotLocalConsoleLib\Models\GoodsTypeEnum;

$guideStartRequest = GuideStartRequestBuilder::init(
    Scenario2Enum::VELOCITY
)
    ->goodsType(
        GoodsTypeEnum::PHYSICAL
    )
    ->build();
```



