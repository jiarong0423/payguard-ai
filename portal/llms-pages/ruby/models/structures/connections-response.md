# Connections Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkNvbm5lY3Rpb25zUmVzcG9uc2U

Deployment mode only. Never a key, a key's presence, a value or a variable name.


# Class Name

`ConnectionsResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `mode` | [`ModeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/mode.md) | Required | Mode. |
| `sandbox_reads` | TrueClass \| FalseClass \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
connections_response = ConnectionsResponse.new(
  ModeEnum::LOCAL,
  true
)
```



