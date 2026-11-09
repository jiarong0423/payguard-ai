# Dispute Amount

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVBbW91bnQ

Dispute amount.


# Class Name

`DisputeAmount`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CurrencyCode` | `string` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `MValue` | `string` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

DisputeAmount disputeAmount = new DisputeAmount
{
    CurrencyCode = "currency_code0",
    MValue = "value6",
};
```



