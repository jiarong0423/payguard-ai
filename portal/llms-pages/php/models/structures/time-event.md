# Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlRpbWVFdmVudA

TimeEvent.


# Class Name

`TimeEvent`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `at` | `string` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` | getAt(): string | setAt(string at): void |
| `kind` | [`string(KindEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/kind.md) | Required | Kind. | getKind(): string | setKind(string kind): void |
| `source` | [`string(Source5Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/source-5.md) | Required | Source. | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\TimeEventBuilder;
use TradeGlotLocalConsoleLib\Models\KindEnum;
use TradeGlotLocalConsoleLib\Models\Source5Enum;

$timeEvent = TimeEventBuilder::init(
    'at6',
    KindEnum::DELIVERY,
    Source5Enum::PROVIDER
)->build();
```



