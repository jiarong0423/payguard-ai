# Session Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlNlc3Npb25SZXNwb25zZQ

SessionResponse.


# Class Name

`SessionResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `csrf_token` | `String` | Required | Csrf token. |
| `expires_at` | `String` | Required | Expires at. |
| `session_id` | `String` | Required | Session id. |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |


# Example

```ruby
session_response = SessionResponse.new(
  'csrf_token8',
  'expires_at4',
  'session_id2',
  'synthetic'
)
```



