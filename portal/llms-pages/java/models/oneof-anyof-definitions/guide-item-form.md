# Guide Item Form

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlSXRlbUZvcm0


# Class Name

`GuideItemForm`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideForm`](http://localhost:3000/llms-pages/java/models/structures/guide-form.md) | GuideItemForm.fromGuideForm(GuideForm guideForm) |


# GuideForm

## Initialization Code

### Example

```java
GuideItemForm.fromGuideForm(
        new GuideForm.Builder(
            Kind2Enum.CHOICE,
            Arrays.asList(
                new GuideOption.Builder(
                    "label2",
                    "value4"
                )
                .build()
            ),
            GuideFormPlaceholder.fromString(
                "String9"
            )
        )
        .build()
    )
```



