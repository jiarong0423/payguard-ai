# Guide Form Request Fields

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3RGaWVsZHM


# Class Name

`GuideFormRequestFields`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`List<GuideField>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/guide-field.md) | GuideFormRequestFields.fromListOfGuideField(List<GuideField> listOfGuideField) |


# List<GuideField>

## Initialization Code

### Example

```java
GuideFormRequestFields.fromListOfGuideField(
        Arrays.asList(
            new GuideField.Builder(
                "item8",
                "value8"
            )
            .build()
        )
    )
```



