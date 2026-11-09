# Policy Context

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlBvbGljeUNvbnRleHQ

PolicyContext.


# Class Name

`PolicyContext`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `as_of` | `str` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `jurisdiction` | `str` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `observation_max_age_days` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/theme.md) | Required | Theme. |


# Example

```python
from tradeglotlocalconsole.models.policy_context import PolicyContext
from tradeglotlocalconsole.models.theme_enum import ThemeEnum

policy_context = PolicyContext(
    as_of='as_of0',
    observation_max_age_days=48,
    theme=ThemeEnum.SOURCE_COMPLIANCE
)
```



