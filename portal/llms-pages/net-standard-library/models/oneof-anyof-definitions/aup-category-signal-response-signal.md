# Aup Category Signal Response Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2VTaWduYWw


# Class Name

`AupCategorySignalResponseSignal`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`CategorySignal`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/category-signal.md) | AupCategorySignalResponseSignal.FromCategorySignal(CategorySignal categorySignal) |


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



