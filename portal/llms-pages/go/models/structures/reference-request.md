# Reference Request

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlcXVlc3Q

ReferenceRequest.


# Class Name

`ReferenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AsOf` | [`*models.ReferenceRequestAsOf`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-request-as-of.md) | Optional | This is a container for any-of cases. |
| `CaseStage` | [`*models.CaseStage2Enum`](http://localhost:3000/llms-pages/go/models/enumerations/case-stage-2.md) | Optional | Case stage.<br><br>**Default**: `"any"` |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `Limit` | `*int` | Optional | Limit.<br><br>**Default**: `3`<br><br>**Constraints**: `>= 1`, `<= 10` |
| `MaterialTypes` | [`*models.ReferenceRequestMaterialTypes`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-request-material-types.md) | Optional | This is a container for any-of cases. |
| `MaxSourceAgeDays` | [`*models.ReferenceRequestMaxSourceAgeDays`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-request-max-source-age-days.md) | Optional | This is a container for any-of cases. |
| `Query` | `string` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` |
| `RequireKnownSourceDate` | `*bool` | Optional | Require known source date.<br><br>**Default**: `false` |
| `Theme` | [`models.ThemeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/theme.md) | Required | Theme. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    referenceRequest := models.ReferenceRequest{
        AsOf:                   models.ToPointer(models.ReferenceRequestAsOfContainer.FromString("String7")),
        CaseStage:              models.ToPointer(models.CaseStage2Enum_ANY),
        Jurisdiction:           "US",
        Limit:                  models.ToPointer(3),
        MaterialTypes:          models.ToPointer(models.ReferenceRequestMaterialTypesContainer.FromArrayOfMaterialType4([]models.MaterialType4Enum{
            models.MaterialType4Enum_PUBLICCOURTORDERCOPY,
        })),
        MaxSourceAgeDays:       models.ToPointer(models.ReferenceRequestMaxSourceAgeDaysContainer.FromNumber(110)),
        Query:                  "query4",
        RequireKnownSourceDate: models.ToPointer(false),
        Theme:                  models.ThemeEnum_DISPUTEMEDIATION,
    }

}
```



