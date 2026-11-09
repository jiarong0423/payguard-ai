# Session Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlNlc3Npb25SZXNwb25zZQ

SessionResponse.


# Class Name

`SessionResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CsrfToken` | `string` | Required | Csrf token. |
| `ExpiresAt` | `string` | Required | Expires at. |
| `SessionId` | `string` | Required | Session id. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    sessionResponse := models.SessionResponse{
        CsrfToken: "csrf_token8",
        ExpiresAt: "expires_at4",
        SessionId: "session_id2",
        Source:    "synthetic",
    }

}
```



