# Guide Form Request Fields

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3RGaWVsZHM


# Class Name

`GuideFormRequestFields`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`List<GuideField>`](http://localhost:3000/llms-pages/java/models/structures/guide-field.md) | GuideFormRequestFields.fromListOfGuideField(List<GuideField> listOfGuideField) |


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



