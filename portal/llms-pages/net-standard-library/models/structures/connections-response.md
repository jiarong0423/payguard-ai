# Connections Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkNvbm5lY3Rpb25zUmVzcG9uc2U

Deployment mode only. Never a key, a key's presence, a value or a variable name.


# Class Name

`ConnectionsResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Mode` | [`ModeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/mode.md) | Required | Mode. |
| `SandboxReads` | [`ConnectionsResponseSandboxReads`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/connections-response-sandbox-reads.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

ConnectionsResponse connectionsResponse = new ConnectionsResponse
{
    Mode = ModeEnum.Local,
    SandboxReads = ConnectionsResponseSandboxReads.FromBoolean(true),
};
```



