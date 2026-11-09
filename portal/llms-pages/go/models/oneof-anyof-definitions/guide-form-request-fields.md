# Guide Form Request Fields

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3RGaWVsZHM


# Class Name

`GuideFormRequestFields`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`[]models.GuideField`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/guide-field.md) | models.GuideFormRequestFieldsContainer.FromArrayOfGuideField([]models.GuideField arrayOfGuideField) |


# []models.GuideField

## Initialization Code

### Example

```go
value := models.GuideFormRequestFieldsContainer.FromArrayOfGuideField([]models.GuideField{
    models.GuideField{
        Item:  "item8",
        Value: "value8",
    },
})
```



