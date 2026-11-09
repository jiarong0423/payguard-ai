# Provider Money

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlByb3ZpZGVyTW9uZXk

ProviderMoney.


# Class Name

`ProviderMoney`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CurrencyCode` | `string` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `MValue` | `string` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

ProviderMoney providerMoney = new ProviderMoney
{
    CurrencyCode = "currency_code4",
    MValue = "value0",
};
```



