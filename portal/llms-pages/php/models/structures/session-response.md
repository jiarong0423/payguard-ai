# Session Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlNlc3Npb25SZXNwb25zZQ

SessionResponse.


# Class Name

`SessionResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `csrfToken` | `string` | Required | Csrf token. | getCsrfToken(): string | setCsrfToken(string csrfToken): void |
| `expiresAt` | `string` | Required | Expires at. | getExpiresAt(): string | setExpiresAt(string expiresAt): void |
| `sessionId` | `string` | Required | Session id. | getSessionId(): string | setSessionId(string sessionId): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\SessionResponseBuilder;

$sessionResponse = SessionResponseBuilder::init(
    'csrf_token8',
    'expires_at4',
    'session_id2'
)->build();
```



