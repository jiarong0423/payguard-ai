# Reference Filters

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlJlZmVyZW5jZUZpbHRlcnM

ReferenceFilters.


# Class Name

`ReferenceFilters`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `age_basis` | `String` | Required, Constant | Age basis.<br><br>**Value**: `'source_updated_date_utc_calendar'` |
| `as_of` | String | Required | This is a container for any-of cases. |
| `case_stage` | [`CaseStage2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/case-stage-2.md) | Required | Case stage. |
| `jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `limit` | `Integer` | Required | Limit.<br><br>**Constraints**: `>= 1`, `<= 10` |
| `material_types` | [`Array[MaterialType4Enum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/material-type-4.md) | Required | Material types.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3` |
| `max_source_age_days` | Integer | Required | This is a container for any-of cases. |
| `require_known_source_date` | `TrueClass \| FalseClass` | Required | Require known source date. |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/theme.md) | Required | Theme. |


# Example

```ruby
reference_filters = ReferenceFilters.new(
  'source_updated_date_utc_calendar',
  'String1',
  CaseStage2Enum::PROCEDURAL_ORDER,
  'US',
  10,
  [
    MaterialType4Enum::OFFICIAL_POLICY,
    MaterialType4Enum::PUBLIC_COURT_ORDER_COPY
  ],
  190,
  false,
  ThemeEnum::DISPUTE_MEDIATION
)
```



