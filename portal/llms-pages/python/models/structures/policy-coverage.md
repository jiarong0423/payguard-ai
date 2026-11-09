# Policy Coverage

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlBvbGljeUNvdmVyYWdl

PolicyCoverage.


# Class Name

`PolicyCoverage`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `basis` | `str` | Required, Constant | Basis.<br><br>**Value**: `"pinned_authored_summaries_only"` |
| `complete` | `bool` | Required | Complete. |
| `missing_official_policy_themes` | [`List[MissingOfficialPolicyThemeEnum]`](http://localhost:3000/llms-pages/python/models/enumerations/missing-official-policy-theme.md) | Required | Missing official policy themes.<br><br>**Constraints**: *Maximum Items*: `3` |
| `official_policy_chunk_count_by_theme` | [`PolicyThemeCounts`](http://localhost:3000/llms-pages/python/models/structures/policy-theme-counts.md) | Required | PolicyThemeCounts. |
| `official_policy_source_ids` | `List[str]` | Required | Official policy source ids.<br><br>**Constraints**: *Maximum Items*: `16`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `regional_source_count` | `int` | Required | Regional source count.<br><br>**Constraints**: `>= 0`, `<= 16` |
| `selected_chunk_count` | `int` | Required | Selected chunk count.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `selected_source_count` | `int` | Required | Selected source count.<br><br>**Constraints**: `>= 0`, `<= 16` |


# Example

```python
from tradeglotlocalconsole.models.missing_official_policy_theme_enum import MissingOfficialPolicyThemeEnum
from tradeglotlocalconsole.models.policy_coverage import PolicyCoverage
from tradeglotlocalconsole.models.policy_theme_counts import PolicyThemeCounts

policy_coverage = PolicyCoverage(
    complete=False,
    missing_official_policy_themes=[
        MissingOfficialPolicyThemeEnum.SOURCE_COMPLIANCE
    ],
    official_policy_chunk_count_by_theme=PolicyThemeCounts(
        dispute_mediation=12,
        source_compliance=29,
        velocity_guard=29
    ),
    official_policy_source_ids=[
        'official_policy_source_ids8'
    ],
    regional_source_count=0,
    selected_chunk_count=29,
    selected_source_count=16
)
```



