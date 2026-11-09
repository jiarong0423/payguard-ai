# Connections Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkNvbm5lY3Rpb25zUmVzcG9uc2U

Deployment mode only. Never a key, a key's presence, a value or a variable name.


# Class Name

`ConnectionsResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Mode` | [`ModeEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/mode.md) | Required | Mode. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

ConnectionsResponse connectionsResponse = new ConnectionsResponse
{
    Mode = ModeEnum.Local,
};
```



