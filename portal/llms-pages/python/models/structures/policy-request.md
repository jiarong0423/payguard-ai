# Policy Request

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlBvbGljeVJlcXVlc3Q

PolicyRequest.


# Class Name

`PolicyRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `as_of` | `str` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `jurisdiction` | `str` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `observation_max_age_days` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/python/models/enumerations/theme.md) | Required | Theme. |


# Example

```python
from tradeglotlocalconsole.models.policy_request import PolicyRequest
from tradeglotlocalconsole.models.theme_enum import ThemeEnum

policy_request = PolicyRequest(
    as_of='as_of2',
    observation_max_age_days=88,
    theme=ThemeEnum.DISPUTE_MEDIATION
)
```



