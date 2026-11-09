# Guide Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlUmVwbHk

GuideReply.


# Class Name

`GuideReply`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Chooser` | [`ChooserEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/chooser.md) | Required | Chooser. | ChooserEnum getChooser() | setChooser(ChooserEnum chooser) |
| `Dropped` | [`List<GuideDropped>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/guide-dropped.md) | Required | Dropped. | List<GuideDropped> getDropped() | setDropped(List<GuideDropped> dropped) |
| `FallbackReason` | [`GuideReplyFallbackReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/guide-reply-fallback-reason.md) | Required | This is a container for any-of cases. | GuideReplyFallbackReason getFallbackReason() | setFallbackReason(GuideReplyFallbackReason fallbackReason) |
| `StateChanged` | `boolean` | Required | State changed. | boolean getStateChanged() | setStateChanged(boolean stateChanged) |
| `Template` | [`TemplateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/template.md) | Required | Template. | TemplateEnum getTemplate() | setTemplate(TemplateEnum template) |
| `Text` | `String` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` | String getText() | setText(String text) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.ChooserEnum;
import m18000.m0.m0.m127.models.FallbackReasonEnum;
import m18000.m0.m0.m127.models.GuideDropped;
import m18000.m0.m0.m127.models.GuideReply;
import m18000.m0.m0.m127.models.Reason6Enum;
import m18000.m0.m0.m127.models.TemplateEnum;
import m18000.m0.m0.m127.models.containers.GuideReplyFallbackReason;

GuideReply guideReply = new GuideReply.Builder(
    ChooserEnum.NONE,
    Arrays.asList(
        new GuideDropped.Builder(
            "item2",
            Reason6Enum.OTHER_PARTY
        )
        .build()
    ),
    GuideReplyFallbackReason.fromFallbackReason(
        FallbackReasonEnum.LATE
    ),
    false,
    TemplateEnum.NO_GUARANTEE,
    "text6"
)
.build();
```



