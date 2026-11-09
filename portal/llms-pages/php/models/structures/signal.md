# Signal

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `category` | string\|null | Optional | This is a container for any-of cases. | getCategory(): ?string | setCategory(?string category): void |
| `confidence` | string([ConfidenceEnum](http://localhost:3000/llms-pages/php/models/enumerations/confidence.md))\|null | Optional | This is a container for any-of cases. | getConfidence(): ?string | setConfidence(?string confidence): void |
| `source` | [`?string(Source2Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/source-2.md) | Optional | Source. | getSource(): ?string | setSource(?string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\SignalBuilder;
use TradeGlotLocalConsoleLib\Models\ConfidenceEnum;
use TradeGlotLocalConsoleLib\Models\Source2Enum;

$signal = SignalBuilder::init()
    ->category(
        'String1'
    )
    ->confidence(
        ConfidenceEnum::HIGH
    )
    ->source(Source2Enum::CHANNEL3)
    ->build();
```



