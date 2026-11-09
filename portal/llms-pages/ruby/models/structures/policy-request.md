# Policy Request

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlBvbGljeVJlcXVlc3Q

PolicyRequest.


# Class Name

`PolicyRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `as_of` | `String` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `observation_max_age_days` | `Integer` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/theme.md) | Required | Theme. |


# Example

```ruby
policy_request = PolicyRequest.new(
  'as_of2',
  'US',
  88,
  ThemeEnum::DISPUTE_MEDIATION
)
```



