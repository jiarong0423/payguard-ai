# Guide Turn Request

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3Q

GuideTurnRequest.


# Class Name

`GuideTurnRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Fields` | [`*models.GuideTurnRequestFields`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-turn-request-fields.md) | Optional | This is a container for any-of cases. |
| `Scenario` | [`*models.GuideTurnRequestScenario`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-turn-request-scenario.md) | Optional | This is a container for any-of cases. |
| `Text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1600` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideTurnRequest := models.GuideTurnRequest{
        Fields:   models.ToPointer(models.GuideTurnRequestFieldsContainer.FromArrayOfGuideField([]models.GuideField{
            models.GuideField{
                Item:  "item8",
                Value: "value8",
            },
        })),
        Scenario: models.ToPointer(models.GuideTurnRequestScenarioContainer.FromScenario1(models.Scenario1Enum_PREFLIGHT)),
        Text:     "text2",
    }

}
```



