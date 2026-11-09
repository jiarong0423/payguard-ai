# Reference Filters

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlJlZmVyZW5jZUZpbHRlcnM

ReferenceFilters.


# Class Name

`ReferenceFilters`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AgeBasis` | `string` | Required, Constant | Age basis.<br><br>**Value**: `"source_updated_date_utc_calendar"` |
| `AsOf` | [`models.ReferenceFiltersAsOf`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-filters-as-of.md) | Required | This is a container for any-of cases. |
| `CaseStage` | [`models.CaseStage2Enum`](http://localhost:3000/llms-pages/go/models/enumerations/case-stage-2.md) | Required | Case stage. |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `Limit` | `int` | Required | Limit.<br><br>**Constraints**: `>= 1`, `<= 10` |
| `MaterialTypes` | [`[]models.MaterialType4Enum`](http://localhost:3000/llms-pages/go/models/enumerations/material-type-4.md) | Required | Material types.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3` |
| `MaxSourceAgeDays` | [`models.ReferenceFiltersMaxSourceAgeDays`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-filters-max-source-age-days.md) | Required | This is a container for any-of cases. |
| `RequireKnownSourceDate` | `bool` | Required | Require known source date. |
| `Theme` | [`models.ThemeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/theme.md) | Required | Theme. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    referenceFilters := models.ReferenceFilters{
        AgeBasis:               "source_updated_date_utc_calendar",
        AsOf:                   models.ReferenceFiltersAsOfContainer.FromString("String9"),
        CaseStage:              models.CaseStage2Enum_PROCEDURALORDER,
        Jurisdiction:           "US",
        Limit:                  10,
        MaterialTypes:          []models.MaterialType4Enum{
            models.MaterialType4Enum_OFFICIALPOLICY,
            models.MaterialType4Enum_PUBLICCOURTORDERCOPY,
        },
        MaxSourceAgeDays:       models.ReferenceFiltersMaxSourceAgeDaysContainer.FromNumber(238),
        RequireKnownSourceDate: false,
        Theme:                  models.ThemeEnum_DISPUTEMEDIATION,
    }

}
```



