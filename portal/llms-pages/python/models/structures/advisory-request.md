# Advisory Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFkdmlzb3J5UmVxdWVzdA

AdvisoryRequest.


# Class Name

`AdvisoryRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `as_of` | `str` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `candidate_json` | `str` | Required | Candidate json.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8192` |
| `jurisdiction` | `str` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `observation_max_age_days` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/theme.md) | Required | Theme. |


# Example

```python
from tradeglotlocalconsole.models.advisory_request import AdvisoryRequest
from tradeglotlocalconsole.models.theme_enum import ThemeEnum

advisory_request = AdvisoryRequest(
    as_of='as_of0',
    candidate_json='candidate_json4',
    observation_max_age_days=214,
    theme=ThemeEnum.SOURCE_COMPLIANCE
)
```



