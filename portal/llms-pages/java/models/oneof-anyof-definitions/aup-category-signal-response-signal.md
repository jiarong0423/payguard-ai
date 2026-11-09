# Aup Category Signal Response Signal

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2VTaWduYWw


# Class Name

`AupCategorySignalResponseSignal`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`CategorySignal`](http://localhost:3000/llms-pages/java/models/structures/category-signal.md) | AupCategorySignalResponseSignal.fromCategorySignal(CategorySignal categorySignal) |


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



