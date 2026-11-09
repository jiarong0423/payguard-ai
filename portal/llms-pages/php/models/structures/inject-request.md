# Inject Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Class Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `scenario` | [`string(Scenario5Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/scenario-5.md) | Required | Scenario. | getScenario(): string | setScenario(string scenario): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\InjectRequestBuilder;
use TradeGlotLocalConsoleLib\Models\Scenario5Enum;

$injectRequest = InjectRequestBuilder::init(
    Scenario5Enum::BURST
)->build();
```



