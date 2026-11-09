# Guide Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlSXRlbQ

GuideItem.


# Class Name

`GuideItem`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Chunk` | [`GuideItemChunk`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/guide-item-chunk.md) | Required | This is a container for any-of cases. | GuideItemChunk getChunk() | setChunk(GuideItemChunk chunk) |
| `Form` | [`GuideItemForm`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/guide-item-form.md) | Required | This is a container for any-of cases. | GuideItemForm getForm() | setForm(GuideItemForm form) |
| `Id` | `String` | Required | Id. | String getId() | setId(String id) |
| `Label` | `String` | Required | Label. | String getLabel() | setLabel(String label) |
| `Source` | [`Source8Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/source-8.md) | Required | Source. | Source8Enum getSource() | setSource(Source8Enum source) |
| `Status` | [`Status9Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/status-9.md) | Required | Status. | Status9Enum getStatus() | setStatus(Status9Enum status) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.GuideForm;
import m18000.m0.m0.m127.models.GuideItem;
import m18000.m0.m0.m127.models.GuideOption;
import m18000.m0.m0.m127.models.Kind2Enum;
import m18000.m0.m0.m127.models.Source8Enum;
import m18000.m0.m0.m127.models.Status9Enum;
import m18000.m0.m0.m127.models.containers.GuideFormPlaceholder;
import m18000.m0.m0.m127.models.containers.GuideItemChunk;
import m18000.m0.m0.m127.models.containers.GuideItemForm;

GuideItem guideItem = new GuideItem.Builder(
    GuideItemChunk.fromString(
        "String7"
    ),
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
    ),
    "id0",
    "label0",
    Source8Enum.OFFICIAL,
    Status9Enum.UNCLEAR
)
.build();
```



