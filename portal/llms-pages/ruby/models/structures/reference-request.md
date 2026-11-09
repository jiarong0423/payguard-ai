# Reference Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlcXVlc3Q

ReferenceRequest.


# Class Name

`ReferenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `as_of` | String \| nil | Optional | This is a container for any-of cases. |
| `case_stage` | [`CaseStage2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/case-stage-2.md) | Optional | Case stage.<br><br>**Default**: `CaseStage2Enum::ANY` |
| `jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `limit` | `Integer` | Optional | Limit.<br><br>**Default**: `3`<br><br>**Constraints**: `>= 1`, `<= 10` |
| `material_types` | Array[[MaterialType4](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/material-type-4.md)] \| nil | Optional | This is a container for any-of cases. |
| `max_source_age_days` | Integer \| nil | Optional | This is a container for any-of cases. |
| `query` | `String` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` |
| `require_known_source_date` | `TrueClass \| FalseClass` | Optional | Require known source date.<br><br>**Default**: `false` |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/theme.md) | Required | Theme. |


# Example

```ruby
reference_request = ReferenceRequest.new(
  'US',
  'query0',
  ThemeEnum::VELOCITY_GUARD,
  'String9',
  CaseStage2Enum::ANY,
  3,
  [
    MaterialType4Enum::OFFICIAL_API_REFERENCE,
    MaterialType4Enum::OFFICIAL_POLICY
  ],
  100,
  false
)
```



