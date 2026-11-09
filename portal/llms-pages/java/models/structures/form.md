# Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkZvcm0

Form.


# Class Name

`Form`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Kind` | [`Kind2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/kind-2.md) | Optional | Kind. | Kind2Enum getKind() | setKind(Kind2Enum kind) |
| `Options` | [`List<GuideOption>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/guide-option.md) | Optional | Options. | List<GuideOption> getOptions() | setOptions(List<GuideOption> options) |
| `Placeholder` | [`FormPlaceholder`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/form-placeholder.md) | Optional | This is a container for any-of cases. | FormPlaceholder getPlaceholder() | setPlaceholder(FormPlaceholder placeholder) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.Form;
import m18000.m0.m0.m127.models.GuideOption;
import m18000.m0.m0.m127.models.Kind2Enum;
import m18000.m0.m0.m127.models.containers.FormPlaceholder;

Form form = new Form.Builder()
    .kind(Kind2Enum.TEXT)
    .options(Arrays.asList(
        new GuideOption.Builder(
            "label2",
            "value4"
        )
        .build(),
        new GuideOption.Builder(
            "label2",
            "value4"
        )
        .build(),
        new GuideOption.Builder(
            "label2",
            "value4"
        )
        .build()
    ))
    .placeholder(FormPlaceholder.fromString(
        "String9"
    ))
    .build();
```



