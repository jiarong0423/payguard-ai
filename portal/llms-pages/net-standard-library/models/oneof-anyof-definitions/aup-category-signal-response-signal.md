# Aup Category Signal Response Signal

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2VTaWduYWw


# Class Name

`AupCategorySignalResponseSignal`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`CategorySignal`](http://localhost:3000/llms-pages/net-standard-library/models/structures/category-signal.md) | AupCategorySignalResponseSignal.FromCategorySignal(CategorySignal categorySignal) |


# CategorySignal

## Initialization Code

### Example

```csharp
AupCategorySignalResponseSignal value = AupCategorySignalResponseSignal.FromCategorySignal(
    new CategorySignal
    {
        Category = CategorySignalCategory.FromString("String9"),
        Confidence = CategorySignalConfidence.FromConfidence(ConfidenceEnum.HIGH),
        Source = "channel3",
    }
);
```



