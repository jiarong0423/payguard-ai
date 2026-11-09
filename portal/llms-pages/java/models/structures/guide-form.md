# Guide Form

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlRm9ybQ

GuideForm.


# Class Name

`GuideForm`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Kind` | [`Kind2Enum`](http://localhost:3000/llms-pages/java/models/enumerations/kind-2.md) | Required | Kind. | Kind2Enum getKind() | setKind(Kind2Enum kind) |
| `Options` | [`List<GuideOption>`](http://localhost:3000/llms-pages/java/models/structures/guide-option.md) | Required | Options. | List<GuideOption> getOptions() | setOptions(List<GuideOption> options) |
| `Placeholder` | [`GuideFormPlaceholder`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-form-placeholder.md) | Required | This is a container for any-of cases. | GuideFormPlaceholder getPlaceholder() | setPlaceholder(GuideFormPlaceholder placeholder) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.GuideForm;
import m18000.m0.m0.m127.models.GuideOption;
import m18000.m0.m0.m127.models.Kind2Enum;
import m18000.m0.m0.m127.models.containers.GuideFormPlaceholder;

GuideForm guideForm = new GuideForm.Builder(
    Kind2Enum.CHOICE,
    Arrays.asList(
        new GuideOption.Builder(
            "label2",
            "value4"
        )
        .build()
    ),
    GuideFormPlaceholder.fromString(
        "String3"
    )
)
.build();
```



