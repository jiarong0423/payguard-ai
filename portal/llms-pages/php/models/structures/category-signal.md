# Category Signal

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkNhdGVnb3J5U2lnbmFs

CategorySignal.


# Class Name

`CategorySignal`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `category` | string | Required | This is a container for any-of cases. | getCategory(): string | setCategory(string category): void |
| `confidence` | string([ConfidenceEnum](http://localhost:3000/llms-pages/php/models/enumerations/confidence.md)) | Required | This is a container for any-of cases. | getConfidence(): string | setConfidence(string confidence): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'channel3'` | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\CategorySignalBuilder;
use TradeGlotLocalConsoleLib\Models\ConfidenceEnum;

$categorySignal = CategorySignalBuilder::init(
    'String1',
    ConfidenceEnum::HIGH
)->build();
```



