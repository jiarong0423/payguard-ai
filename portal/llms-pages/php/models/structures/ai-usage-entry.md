# Ai Usage Entry

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkFpVXNhZ2VFbnRyeQ

AiUsageEntry.


# Class Name

`AiUsageEntry`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `at` | `string` | Required | At. | getAt(): string | setAt(string at): void |
| `estimatedCostUsd` | string\|null | Optional | This is a container for any-of cases. | getEstimatedCostUsd(): ?string | setEstimatedCostUsd(?string estimatedCostUsd): void |
| `latencyMs` | `int` | Required | Latency ms.<br><br>**Constraints**: `>= 0`, `<= 3600000` | getLatencyMs(): int | setLatencyMs(int latencyMs): void |
| `model` | string\|null | Optional | This is a container for any-of cases. | getModel(): ?string | setModel(?string model): void |
| `outcome` | [`string(OutcomeEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/outcome.md) | Required | Outcome. | getOutcome(): string | setOutcome(string outcome): void |
| `stage` | [`string(Stage2Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/stage-2.md) | Required | Stage. | getStage(): string | setStage(string stage): void |
| `tokensIn` | int\|null | Optional | This is a container for any-of cases. | getTokensIn(): ?int | setTokensIn(?int tokensIn): void |
| `tokensOut` | int\|null | Optional | This is a container for any-of cases. | getTokensOut(): ?int | setTokensOut(?int tokensOut): void |
| `tokensTotal` | int\|null | Optional | This is a container for any-of cases. | getTokensTotal(): ?int | setTokensTotal(?int tokensTotal): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AiUsageEntryBuilder;
use TradeGlotLocalConsoleLib\Models\OutcomeEnum;
use TradeGlotLocalConsoleLib\Models\Stage2Enum;

$aiUsageEntry = AiUsageEntryBuilder::init(
    'at4',
    38,
    OutcomeEnum::OK,
    Stage2Enum::VELOCITY_GUARD
)
    ->estimatedCostUsd(
        'String5'
    )
    ->model(
        'String7'
    )
    ->tokensIn(
        236
    )
    ->tokensOut(
        94
    )
    ->tokensTotal(
        158
    )
    ->build();
```



