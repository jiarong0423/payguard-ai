# Guide State Response Form Result

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZUZvcm1SZXN1bHQ


# Class Name

`GuideStateResponseFormResult`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.GuideFormResult`](http://localhost:3000/llms-pages/go/models/structures/guide-form-result.md) | models.GuideStateResponseFormResultContainer.FromGuideFormResult(models.GuideFormResult guideFormResult) |


# models.GuideFormResult

## Initialization Code

### Example

```go
value := models.GuideStateResponseFormResultContainer.FromGuideFormResult(models.GuideFormResult{
    Item:  "item2",
    Valid: false,
})
```



