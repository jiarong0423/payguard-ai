# Guide Item Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlSXRlbUZvcm0


# Class Name

`GuideItemForm`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideForm`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/guide-form.md) | GuideItemForm.fromGuideForm(GuideForm guideForm) |


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



