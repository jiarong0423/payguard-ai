# Aup Category Signal Response Signal

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2VTaWduYWw


# Class Name

`AupCategorySignalResponseSignal`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.CategorySignal`](http://localhost:3000/llms-pages/go/models/structures/category-signal.md) | models.AupCategorySignalResponseSignalContainer.FromCategorySignal(models.CategorySignal categorySignal) |


# models.CategorySignal

## Initialization Code

### Example

```go
value := models.AupCategorySignalResponseSignalContainer.FromCategorySignal(models.CategorySignal{
    Category:             models.CategorySignalCategoryContainer.FromString("String9"),
    Confidence:           models.CategorySignalConfidenceContainer.FromConfidence(models.ConfidenceEnum_HIGH),
    Source:               "channel3",
})
```



