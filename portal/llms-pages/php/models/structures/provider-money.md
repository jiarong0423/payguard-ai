# Provider Money

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlByb3ZpZGVyTW9uZXk

ProviderMoney.


# Class Name

`ProviderMoney`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `currencyCode` | `string` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` | getCurrencyCode(): string | setCurrencyCode(string currencyCode): void |
| `value` | `string` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` | getValue(): string | setValue(string value): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ProviderMoneyBuilder;

$providerMoney = ProviderMoneyBuilder::init(
    'currency_code4',
    'value0'
)->build();
```



