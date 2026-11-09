# Policy Coverage

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlBvbGljeUNvdmVyYWdl

PolicyCoverage.


# Class Name

`PolicyCoverage`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `basis` | `String` | Required, Constant | Basis.<br><br>**Value**: `'pinned_authored_summaries_only'` |
| `complete` | `TrueClass \| FalseClass` | Required | Complete. |
| `missing_official_policy_themes` | [`Array[MissingOfficialPolicyThemeEnum]`](http://localhost:3000/llms-pages/ruby/models/enumerations/missing-official-policy-theme.md) | Required | Missing official policy themes.<br><br>**Constraints**: *Maximum Items*: `3` |
| `official_policy_chunk_count_by_theme` | [`PolicyThemeCounts`](http://localhost:3000/llms-pages/ruby/models/structures/policy-theme-counts.md) | Required | PolicyThemeCounts. |
| `official_policy_source_ids` | `Array[String]` | Required | Official policy source ids.<br><br>**Constraints**: *Maximum Items*: `16`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `regional_source_count` | `Integer` | Required | Regional source count.<br><br>**Constraints**: `>= 0`, `<= 16` |
| `selected_chunk_count` | `Integer` | Required | Selected chunk count.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `selected_source_count` | `Integer` | Required | Selected source count.<br><br>**Constraints**: `>= 0`, `<= 16` |


# Example

```ruby
policy_coverage = PolicyCoverage.new(
  'pinned_authored_summaries_only',
  false,
  [
    MissingOfficialPolicyThemeEnum::SOURCE_COMPLIANCE
  ],
  PolicyThemeCounts.new(
    12,
    29,
    29
  ),
  [
    'official_policy_source_ids8'
  ],
  0,
  29,
  16
)
```



