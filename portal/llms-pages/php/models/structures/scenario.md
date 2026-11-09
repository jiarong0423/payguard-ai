# Scenario

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlNjZW5hcmlv

Scenario.


# Class Name

`Scenario`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `burst` | `bool` | Required | Burst. | getBurst(): bool | setBurst(bool burst): void |
| `dispute` | `bool` | Required | Dispute. | getDispute(): bool | setDispute(bool dispute): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ScenarioBuilder;

$scenario = ScenarioBuilder::init(
    false,
    false
)->build();
```



