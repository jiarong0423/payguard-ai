# Ai Usage Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkFpVXNhZ2VSZXNwb25zZQ

AiUsageResponse.


# Class Name

`AiUsageResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `contentLogged` | `?bool` | Optional | Content logged.<br><br>**Default**: `false` | getContentLogged(): ?bool | setContentLogged(?bool contentLogged): void |
| `costNote` | `string` | Required | Cost note. | getCostNote(): string | setCostNote(string costNote): void |
| `entries` | [`AiUsageEntry[]`](http://localhost:3000/llms-pages/php/models/structures/ai-usage-entry.md) | Required | Entries.<br><br>**Constraints**: *Maximum Items*: `50` | getEntries(): array | setEntries(array entries): void |
| `priceTableSource` | `string` | Required | Price table source. | getPriceTableSource(): string | setPriceTableSource(string priceTableSource): void |
| `source` | [`string(Source1Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/source-1.md) | Required | Source. | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AiUsageResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\AiUsageEntryBuilder;
use TradeGlotLocalConsoleLib\Models\OutcomeEnum;
use TradeGlotLocalConsoleLib\Models\Stage2Enum;
use TradeGlotLocalConsoleLib\Models\Source1Enum;

$aiUsageResponse = AiUsageResponseBuilder::init(
    'cost_note4',
    [
        AiUsageEntryBuilder::init(
            'at6',
            254,
            OutcomeEnum::OK,
            Stage2Enum::STUDIO_AGENT
        )
            ->estimatedCostUsd(
                'String7'
            )
            ->model(
                'String9'
            )
            ->tokensIn(
                196
            )
            ->tokensOut(
                54
            )
            ->tokensTotal(
                118
            )
            ->build()
    ],
    'price_table_source0',
    Source1Enum::SESSION_MEMORY
)
    ->contentLogged(false)
    ->build();
```



