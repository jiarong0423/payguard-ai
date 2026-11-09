# Advisory Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkFkdmlzb3J5UmVxdWVzdA

AdvisoryRequest.


# Class Name

`AdvisoryRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `as_of` | `String` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `candidate_json` | `String` | Required | Candidate json.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8192` |
| `jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `observation_max_age_days` | `Integer` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/theme.md) | Required | Theme. |


# Example

```ruby
advisory_request = AdvisoryRequest.new(
  'as_of0',
  'candidate_json4',
  'US',
  214,
  ThemeEnum::SOURCE_COMPLIANCE
)
```



