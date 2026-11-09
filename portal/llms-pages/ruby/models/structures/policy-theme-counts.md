# Policy Theme Counts

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlBvbGljeVRoZW1lQ291bnRz

PolicyThemeCounts.


# Class Name

`PolicyThemeCounts`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `dispute_mediation` | `Integer` | Required | Dispute mediation.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `source_compliance` | `Integer` | Required | Source compliance.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `velocity_guard` | `Integer` | Required | Velocity guard.<br><br>**Constraints**: `>= 0`, `<= 29` |


# Example

```ruby
policy_theme_counts = PolicyThemeCounts.new(
  29,
  29,
  29
)
```



