# Reference Filters

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlJlZmVyZW5jZUZpbHRlcnM

ReferenceFilters.


# Class Name

`ReferenceFilters`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `age_basis` | `str` | Required, Constant | Age basis.<br><br>**Value**: `"source_updated_date_utc_calendar"` |
| `as_of` | str | Required | This is a container for any-of cases. |
| `case_stage` | [`CaseStage2Enum`](http://localhost:3000/llms-pages/python/models/enumerations/case-stage-2.md) | Required | Case stage. |
| `jurisdiction` | `str` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `limit` | `int` | Required | Limit.<br><br>**Constraints**: `>= 1`, `<= 10` |
| `material_types` | [`List[MaterialType4Enum]`](http://localhost:3000/llms-pages/python/models/enumerations/material-type-4.md) | Required | Material types.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3` |
| `max_source_age_days` | int | Required | This is a container for any-of cases. |
| `require_known_source_date` | `bool` | Required | Require known source date. |
| `theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/python/models/enumerations/theme.md) | Required | Theme. |


# Example

```python
from tradeglotlocalconsole.models.case_stage_2_enum import CaseStage2Enum
from tradeglotlocalconsole.models.material_type_4_enum import MaterialType4Enum
from tradeglotlocalconsole.models.reference_filters import ReferenceFilters
from tradeglotlocalconsole.models.theme_enum import ThemeEnum

reference_filters = ReferenceFilters(
    as_of='String1',
    case_stage=CaseStage2Enum.PROCEDURAL_ORDER,
    limit=10,
    material_types=[
        MaterialType4Enum.OFFICIAL_POLICY,
        MaterialType4Enum.PUBLIC_COURT_ORDER_COPY
    ],
    max_source_age_days=190,
    require_known_source_date=False,
    theme=ThemeEnum.DISPUTE_MEDIATION
)
```



