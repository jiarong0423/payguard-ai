# Aup Category Signal Response Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2VTaWduYWw


# Class Name

`AupCategorySignalResponseSignal`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.CategorySignal`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/category-signal.md) | models.AupCategorySignalResponseSignalContainer.FromCategorySignal(models.CategorySignal categorySignal) |


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



