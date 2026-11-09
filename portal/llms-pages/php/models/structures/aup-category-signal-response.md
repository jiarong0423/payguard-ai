# Aup Category Signal Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2U

Optional Channel3 signal shown next to the AUP result; it never changes the rule decision.


# Class Name

`AupCategorySignalResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `affectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` | getAffectsDecision(): string | setAffectsDecision(string affectsDecision): void |
| `reason` | string([ReasonEnum](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/reason.md)) | Required | This is a container for any-of cases. | getReason(): string | setReason(string reason): void |
| `signal` | [CategorySignal](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/category-signal.md) | Required | This is a container for any-of cases. | getSignal(): CategorySignal | setSignal(CategorySignal signal): void |
| `status` | [`string(Status2Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/status-2.md) | Required | Status. | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AupCategorySignalResponseBuilder;
use TradeGlotLocalConsoleLib\Models\ReasonEnum;
use TradeGlotLocalConsoleLib\Models\Builders\CategorySignalBuilder;
use TradeGlotLocalConsoleLib\Models\ConfidenceEnum;
use TradeGlotLocalConsoleLib\Models\Status2Enum;

$aupCategorySignalResponse = AupCategorySignalResponseBuilder::init(
    ReasonEnum::BUDGET_EXHAUSTED,
    CategorySignalBuilder::init(
        'String9',
        ConfidenceEnum::HIGH
    )->build(),
    Status2Enum::NOT_SENT
)->build();
```



