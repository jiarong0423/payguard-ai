# Reply

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlJlcGx5

Reply.


# Class Name

`Reply`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Chooser` | [`ChooserEnum`](http://localhost:3000/llms-pages/java/models/enumerations/chooser.md) | Optional | Chooser. | ChooserEnum getChooser() | setChooser(ChooserEnum chooser) |
| `Dropped` | [`List<GuideDropped>`](http://localhost:3000/llms-pages/java/models/structures/guide-dropped.md) | Optional | Dropped. | List<GuideDropped> getDropped() | setDropped(List<GuideDropped> dropped) |
| `FallbackReason` | [`ReplyFallbackReason`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/reply-fallback-reason.md) | Optional | This is a container for any-of cases. | ReplyFallbackReason getFallbackReason() | setFallbackReason(ReplyFallbackReason fallbackReason) |
| `StateChanged` | `Boolean` | Optional | State changed. | Boolean getStateChanged() | setStateChanged(Boolean stateChanged) |
| `Template` | [`TemplateEnum`](http://localhost:3000/llms-pages/java/models/enumerations/template.md) | Optional | Template. | TemplateEnum getTemplate() | setTemplate(TemplateEnum template) |
| `Text` | `String` | Optional | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` | String getText() | setText(String text) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.ChooserEnum;
import m18000.m0.m0.m127.models.FallbackReasonEnum;
import m18000.m0.m0.m127.models.GuideDropped;
import m18000.m0.m0.m127.models.Reason6Enum;
import m18000.m0.m0.m127.models.Reply;
import m18000.m0.m0.m127.models.TemplateEnum;
import m18000.m0.m0.m127.models.containers.ReplyFallbackReason;

Reply reply = new Reply.Builder()
    .chooser(ChooserEnum.KEYWORD)
    .dropped(Arrays.asList(
        new GuideDropped.Builder(
            "item2",
            Reason6Enum.OTHER_PARTY
        )
        .build(),
        new GuideDropped.Builder(
            "item2",
            Reason6Enum.OTHER_PARTY
        )
        .build()
    ))
    .fallbackReason(ReplyFallbackReason.fromFallbackReason(
        FallbackReasonEnum.PROVIDER_ERROR
    ))
    .stateChanged(false)
    .template(TemplateEnum.SUBTRACTION)
    .build();
```



