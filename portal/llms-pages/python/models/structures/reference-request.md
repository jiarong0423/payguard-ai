# Reference Request

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlcXVlc3Q

ReferenceRequest.


# Class Name

`ReferenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `as_of` | str \| None | Optional | This is a container for any-of cases. |
| `case_stage` | [`CaseStage2Enum`](http://localhost:3000/llms-pages/python/models/enumerations/case-stage-2.md) | Optional | Case stage.<br><br>**Default**: `"any"` |
| `jurisdiction` | `str` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `limit` | `int` | Optional | Limit.<br><br>**Default**: `3`<br><br>**Constraints**: `>= 1`, `<= 10` |
| `material_types` | List[[MaterialType4](http://localhost:3000/llms-pages/python/models/enumerations/material-type-4.md)] \| None | Optional | This is a container for any-of cases. |
| `max_source_age_days` | int \| None | Optional | This is a container for any-of cases. |
| `query` | `str` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` |
| `require_known_source_date` | `bool` | Optional | Require known source date.<br><br>**Default**: `False` |
| `theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/python/models/enumerations/theme.md) | Required | Theme. |


# Example

```python
from tradeglotlocalconsole.models.case_stage_2_enum import CaseStage2Enum
from tradeglotlocalconsole.models.material_type_4_enum import MaterialType4Enum
from tradeglotlocalconsole.models.reference_request import ReferenceRequest
from tradeglotlocalconsole.models.theme_enum import ThemeEnum

reference_request = ReferenceRequest(
    query='query0',
    theme=ThemeEnum.VELOCITY_GUARD,
    as_of='String9',
    case_stage=CaseStage2Enum.ANY,
    limit=3,
    material_types=[
        MaterialType4Enum.OFFICIAL_API_REFERENCE,
        MaterialType4Enum.OFFICIAL_POLICY
    ],
    max_source_age_days=100,
    require_known_source_date=False
)
```



