# Ai Brief Http Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkFpQnJpZWZIdHRwUmVxdWVzdA

What the console may send: the stage and, for disputes, which case. Session facts are never caller input.


# Class Name

`AiBriefHttpRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `caseRef` | string\|null | Optional | This is a container for any-of cases. | getCaseRef(): ?string | setCaseRef(?string caseRef): void |
| `stage` | [`string(StageEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/stage.md) | Required | Stage. | getStage(): string | setStage(string stage): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AiBriefHttpRequestBuilder;
use TradeGlotLocalConsoleLib\Models\StageEnum;

$aiBriefHttpRequest = AiBriefHttpRequestBuilder::init(
    StageEnum::VELOCITY_GUARD
)
    ->caseRef(
        'String9'
    )
    ->build();
```



