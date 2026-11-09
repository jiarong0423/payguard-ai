# Guide Turn Request Fields

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3RGaWVsZHM


# Class Name

`GuideTurnRequestFields`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`List<GuideField>`](http://localhost:3000/llms-pages/java/models/structures/guide-field.md) | GuideTurnRequestFields.fromListOfGuideField(List<GuideField> listOfGuideField) |


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



