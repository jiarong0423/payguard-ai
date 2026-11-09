# Guide Form Request

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3Q

One field ({item, value}) or one round of up to three fields ({fields: [...]}), never both.


# Class Name

`GuideFormRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ConfirmReview` | `*bool` | Optional | Confirm review.<br><br>**Default**: `false` |
| `Fields` | [`*models.GuideFormRequestFields`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-form-request-fields.md) | Optional | This is a container for any-of cases. |
| `Item` | [`*models.GuideFormRequestItem`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-form-request-item.md) | Optional | This is a container for any-of cases. |
| `Scenario` | [`*models.GuideFormRequestScenario`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-form-request-scenario.md) | Optional | This is a container for any-of cases. |
| `Value` | [`*models.GuideFormRequestValue`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-form-request-value.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideFormRequest := models.GuideFormRequest{
        ConfirmReview: models.ToPointer(false),
        Fields:        models.ToPointer(models.GuideFormRequestFieldsContainer.FromArrayOfGuideField([]models.GuideField{
            models.GuideField{
                Item:  "item8",
                Value: "value8",
            },
        })),
        Item:          models.ToPointer(models.GuideFormRequestItemContainer.FromString("String1")),
        Scenario:      models.ToPointer(models.GuideFormRequestScenarioContainer.FromScenario1(models.Scenario1Enum_PREFLIGHT)),
        Value:         models.ToPointer(models.GuideFormRequestValueContainer.FromString("String1")),
    }

}
```



