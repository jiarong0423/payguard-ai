# Analysis

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkFuYWx5c2lz

Analysis.


# Class Name

`Analysis`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `reason` | string([Reason5Enum](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/reason-5.md))\|null | Optional | This is a container for any-of cases. | getReason(): ?string | setReason(?string reason): void |
| `status` | [`?string(Status8Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/status-8.md) | Optional | Status. | getStatus(): ?string | setStatus(?string status): void |
| `turn` | `?int` | Optional | Turn. | getTurn(): ?int | setTurn(?int turn): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AnalysisBuilder;
use TradeGlotLocalConsoleLib\Models\Reason5Enum;
use TradeGlotLocalConsoleLib\Models\Status8Enum;

$analysis = AnalysisBuilder::init()
    ->reason(
        Reason5Enum::INVALID_REPLY
    )
    ->status(Status8Enum::REPLACED)
    ->turn(198)
    ->build();
```



