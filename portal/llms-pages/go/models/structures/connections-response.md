# Connections Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkNvbm5lY3Rpb25zUmVzcG9uc2U

Deployment mode only. Never a key, a key's presence, a value or a variable name.


# Class Name

`ConnectionsResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Mode` | [`models.ModeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/mode.md) | Required | Mode. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    connectionsResponse := models.ConnectionsResponse{
        Mode: models.ModeEnum_LOCAL,
    }

}
```



