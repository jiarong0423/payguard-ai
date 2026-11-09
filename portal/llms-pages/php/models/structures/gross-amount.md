# Gross Amount

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkdyb3NzQW1vdW50

Gross amount.


# Class Name

`GrossAmount`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `currencyCode` | `?string` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` | getCurrencyCode(): ?string | setCurrencyCode(?string currencyCode): void |
| `value` | `?string` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` | getValue(): ?string | setValue(?string value): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GrossAmountBuilder;

$grossAmount = GrossAmountBuilder::init()
    ->currencyCode('currency_code6')
    ->value('value2')
    ->build();
```



