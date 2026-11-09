# Guide Item Form

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlSXRlbUZvcm0


# Class Name

`GuideItemForm`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.GuideForm`](http://localhost:3000/llms-pages/go/models/structures/guide-form.md) | models.GuideItemFormContainer.FromGuideForm(models.GuideForm guideForm) |


# models.GuideForm

## Initialization Code

### Example

```go
value := models.GuideItemFormContainer.FromGuideForm(models.GuideForm{
    Kind:        models.Kind2Enum_CHOICE,
    Options:     []models.GuideOption{
        models.GuideOption{
            Label: "label2",
            Value: "value4",
        },
    },
    Placeholder: models.GuideFormPlaceholderContainer.FromString("String9"),
})
```



