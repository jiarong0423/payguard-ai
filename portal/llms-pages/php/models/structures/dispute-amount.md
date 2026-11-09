# Dispute Amount

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVBbW91bnQ

Dispute amount.


# Class Name

`DisputeAmount`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `currencyCode` | `?string` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` | getCurrencyCode(): ?string | setCurrencyCode(?string currencyCode): void |
| `value` | `?string` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` | getValue(): ?string | setValue(?string value): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeAmountBuilder;

$disputeAmount = DisputeAmountBuilder::init()
    ->currencyCode('currency_code0')
    ->value('value6')
    ->build();
```



