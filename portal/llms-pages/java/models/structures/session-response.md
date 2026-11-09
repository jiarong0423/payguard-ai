# Session Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlNlc3Npb25SZXNwb25zZQ

SessionResponse.


# Class Name

`SessionResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CsrfToken` | `String` | Required | Csrf token. | String getCsrfToken() | setCsrfToken(String csrfToken) |
| `ExpiresAt` | `String` | Required | Expires at. | String getExpiresAt() | setExpiresAt(String expiresAt) |
| `SessionId` | `String` | Required | Session id. | String getSessionId() | setSessionId(String sessionId) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |


# Example

```java
import m18000.m0.m0.m127.models.SessionResponse;

SessionResponse sessionResponse = new SessionResponse.Builder(
    "csrf_token8",
    "expires_at4",
    "session_id2",
    "synthetic"
)
.build();
```



