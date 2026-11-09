# Guide Form Request Fields

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3RGaWVsZHM


# Class Name

`GuideFormRequestFields`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`[]models.GuideField`](http://localhost:3000/llms-pages/go/models/structures/guide-field.md) | models.GuideFormRequestFieldsContainer.FromArrayOfGuideField([]models.GuideField arrayOfGuideField) |


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



