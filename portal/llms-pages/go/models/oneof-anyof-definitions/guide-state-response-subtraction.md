# Guide State Response Subtraction

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVN1YnRyYWN0aW9u


# Class Name

`GuideStateResponseSubtraction`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.GuideSubtraction`](http://localhost:3000/llms-pages/go/models/structures/guide-subtraction.md) | models.GuideStateResponseSubtractionContainer.FromGuideSubtraction(models.GuideSubtraction guideSubtraction) |


# models.GuideSubtraction

## Initialization Code

### Example

```go
value := models.GuideStateResponseSubtractionContainer.FromGuideSubtraction(models.GuideSubtraction{
    Left:                 64,
    Needed:               190,
    Taken:                178,
    Text:                 "text0",
})
```



