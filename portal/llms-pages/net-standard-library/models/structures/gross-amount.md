# Gross Amount

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkdyb3NzQW1vdW50

Gross amount.


# Class Name

`GrossAmount`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CurrencyCode` | `string` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `MValue` | `string` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

GrossAmount grossAmount = new GrossAmount
{
    CurrencyCode = "currency_code6",
    MValue = "value2",
};
```



