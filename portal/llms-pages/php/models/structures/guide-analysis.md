# Guide Analysis

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlQW5hbHlzaXM

GuideAnalysis.


# Class Name

`GuideAnalysis`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `reason` | string([Reason5Enum](http://localhost:3000/llms-pages/php/models/enumerations/reason-5.md)) | Required | This is a container for any-of cases. | getReason(): string | setReason(string reason): void |
| `status` | [`string(Status8Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/status-8.md) | Required | Status. | getStatus(): string | setStatus(string status): void |
| `turn` | `int` | Required | Turn. | getTurn(): int | setTurn(int turn): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideAnalysisBuilder;
use TradeGlotLocalConsoleLib\Models\Reason5Enum;
use TradeGlotLocalConsoleLib\Models\Status8Enum;

$guideAnalysis = GuideAnalysisBuilder::init(
    Reason5Enum::INVALID_REPLY,
    Status8Enum::ANALYSING,
    236
)->build();
```



