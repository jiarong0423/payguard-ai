# Connections Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkNvbm5lY3Rpb25zUmVzcG9uc2U

Deployment mode only. Never a key, a key's presence, a value or a variable name.


# Class Name

`ConnectionsResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Mode` | [`models.ModeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/mode.md) | Required | Mode. |
| `SandboxReads` | [`*models.ConnectionsResponseSandboxReads`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/connections-response-sandbox-reads.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    connectionsResponse := models.ConnectionsResponse{
        Mode:         models.ModeEnum_LOCAL,
        SandboxReads: models.ToPointer(models.ConnectionsResponseSandboxReadsContainer.FromBoolean(true)),
    }

}
```



