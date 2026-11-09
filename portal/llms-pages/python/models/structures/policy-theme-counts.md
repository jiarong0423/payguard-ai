# Policy Theme Counts

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlBvbGljeVRoZW1lQ291bnRz

PolicyThemeCounts.


# Class Name

`PolicyThemeCounts`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `dispute_mediation` | `int` | Required | Dispute mediation.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `source_compliance` | `int` | Required | Source compliance.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `velocity_guard` | `int` | Required | Velocity guard.<br><br>**Constraints**: `>= 0`, `<= 29` |


# Example

```python
from tradeglotlocalconsole.models.policy_theme_counts import PolicyThemeCounts

policy_theme_counts = PolicyThemeCounts(
    dispute_mediation=29,
    source_compliance=29,
    velocity_guard=29
)
```



