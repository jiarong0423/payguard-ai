# Aup Category Signal Response Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2VTaWduYWw


# Class Name

`AupCategorySignalResponseSignal`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`CategorySignal`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/category-signal.md) | AupCategorySignalResponseSignal.fromCategorySignal(CategorySignal categorySignal) |


# CategorySignal

## Initialization Code

### Example

```java
AupCategorySignalResponseSignal.fromCategorySignal(
        new CategorySignal.Builder(
            CategorySignalCategory.fromString(
                "String9"
            ),
            CategorySignalConfidence.fromConfidence(
                ConfidenceEnum.HIGH
            ),
            "channel3"
        )
        .build()
    )
```



