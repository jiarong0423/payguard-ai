# Policy Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlBvbGljeVJlcXVlc3Q

PolicyRequest.


# Class Name

`PolicyRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AsOf` | `string` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `ObservationMaxAgeDays` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `Theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/theme.md) | Required | Theme. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

PolicyRequest policyRequest = new PolicyRequest
{
    AsOf = "as_of8",
    Jurisdiction = "US",
    ObservationMaxAgeDays = 186,
    Theme = ThemeEnum.DisputeMediation,
};
```



