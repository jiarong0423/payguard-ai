# Session Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlNlc3Npb25SZXNwb25zZQ

SessionResponse.


# Interface Name

`SessionResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `csrfToken` | `string` | Required | Csrf token. |
| `expiresAt` | `string` | Required | Expires at. |
| `sessionId` | `string` | Required | Session id. |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |


# Example

```ts
import { SessionResponse } from 'tradeglot-local-consolelib';

const sessionResponse: SessionResponse = {
  csrfToken: 'csrf_token8',
  expiresAt: 'expires_at4',
  sessionId: 'session_id2',
  source: 'synthetic',
};
```



