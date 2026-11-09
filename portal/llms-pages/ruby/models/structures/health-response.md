# Health Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkhlYWx0aFJlc3BvbnNl

HealthResponse.


# Class Name

`HealthResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `mode` | `String` | Required, Constant | Mode.<br><br>**Value**: `'demo'` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `status` | `String` | Required, Constant | Status.<br><br>**Value**: `'ok'` |
| `version` | `String` | Required | Version. |


# Example

```ruby
health_response = HealthResponse.new(
  'demo',
  'synthetic',
  'ok',
  'version2'
)
```



