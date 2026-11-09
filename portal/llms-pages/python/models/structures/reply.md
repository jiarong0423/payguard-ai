# Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlJlcGx5

Reply.


# Class Name

`Reply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chooser` | [`ChooserEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/chooser.md) | Optional | Chooser. |
| `dropped` | [`List[GuideDropped]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/guide-dropped.md) | Optional | Dropped. |
| `fallback_reason` | [FallbackReason](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/fallback-reason.md) \| None | Optional | This is a container for any-of cases. |
| `state_changed` | `bool` | Optional | State changed. |
| `template` | [`TemplateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/template.md) | Optional | Template. |
| `text` | `str` | Optional | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```python
from tradeglotlocalconsole.models.chooser_enum import ChooserEnum
from tradeglotlocalconsole.models.fallback_reason_enum import FallbackReasonEnum
from tradeglotlocalconsole.models.guide_dropped import GuideDropped
from tradeglotlocalconsole.models.reason_6_enum import Reason6Enum
from tradeglotlocalconsole.models.reply import Reply
from tradeglotlocalconsole.models.template_enum import TemplateEnum

reply = Reply(
    chooser=ChooserEnum.KEYWORD,
    dropped=[
        GuideDropped(
            item='item2',
            reason=Reason6Enum.OTHER_PARTY
        ),
        GuideDropped(
            item='item2',
            reason=Reason6Enum.OTHER_PARTY
        )
    ],
    fallback_reason=FallbackReasonEnum.PROVIDER_ERROR,
    state_changed=False,
    template=TemplateEnum.SUBTRACTION
)
```



