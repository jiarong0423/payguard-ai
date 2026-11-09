# Guide Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkd1aWRlUmVwbHk

GuideReply.


# Class Name

`GuideReply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chooser` | [`ChooserEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/chooser.md) | Required | Chooser. |
| `dropped` | [`List[GuideDropped]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/guide-dropped.md) | Required | Dropped. |
| `fallback_reason` | [FallbackReason](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/fallback-reason.md) | Required | This is a container for any-of cases. |
| `state_changed` | `bool` | Required | State changed. |
| `template` | [`TemplateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/template.md) | Required | Template. |
| `text` | `str` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```python
from tradeglotlocalconsole.models.chooser_enum import ChooserEnum
from tradeglotlocalconsole.models.fallback_reason_enum import FallbackReasonEnum
from tradeglotlocalconsole.models.guide_dropped import GuideDropped
from tradeglotlocalconsole.models.guide_reply import GuideReply
from tradeglotlocalconsole.models.reason_6_enum import Reason6Enum
from tradeglotlocalconsole.models.template_enum import TemplateEnum

guide_reply = GuideReply(
    chooser=ChooserEnum.MODEL,
    dropped=[
        GuideDropped(
            item='item2',
            reason=Reason6Enum.OTHER_PARTY
        )
    ],
    fallback_reason=FallbackReasonEnum.BUDGET,
    state_changed=False,
    template=TemplateEnum.OTHER_PARTY,
    text='text2'
)
```



