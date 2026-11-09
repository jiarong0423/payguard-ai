# Health Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkhlYWx0aFJlc3BvbnNl

HealthResponse.


# Class Name

`HealthResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Mode` | `string` | Required, Constant | Mode.<br><br>**Value**: `"demo"` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"ok"` |
| `Version` | `string` | Required | Version. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

HealthResponse healthResponse = new HealthResponse
{
    Mode = "demo",
    Source = "synthetic",
    Status = "ok",
    Version = "version0",
};
```



