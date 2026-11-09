# Guide Turn Request Fields

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3RGaWVsZHM


# Class Name

`GuideTurnRequestFields`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`List<GuideField>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/guide-field.md) | GuideTurnRequestFields.fromListOfGuideField(List<GuideField> listOfGuideField) |


# List<GuideField>

## Initialization Code

### Example

```java
GuideTurnRequestFields.fromListOfGuideField(
        Arrays.asList(
            new GuideField.Builder(
                "item8",
                "value8"
            )
            .build()
        )
    )
```



