# Ai Brief Http Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFpQnJpZWZIdHRwUmVxdWVzdA

What the console may send: the stage and, for disputes, which case. Session facts are never caller input.


# Class Name

`AiBriefHttpRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | str \| None | Optional | This is a container for any-of cases. |
| `stage` | [`StageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/stage.md) | Required | Stage. |


# Example

```python
from tradeglotlocalconsole.models.ai_brief_http_request import AiBriefHttpRequest
from tradeglotlocalconsole.models.stage_enum import StageEnum

ai_brief_http_request = AiBriefHttpRequest(
    stage=StageEnum.DISPUTE_MEDIATION,
    case_ref='String7'
)
```



