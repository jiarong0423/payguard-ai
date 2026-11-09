# Synthetic Money

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlN5bnRoZXRpY01vbmV5

Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic.


# Class Name

`SyntheticMoney`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CurrencyCode` | `string` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `MValue` | `string` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

SyntheticMoney syntheticMoney = new SyntheticMoney
{
    CurrencyCode = "currency_code8",
    MValue = "value4",
};
```



