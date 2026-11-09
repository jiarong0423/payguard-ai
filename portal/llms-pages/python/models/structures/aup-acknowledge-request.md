# Aup Acknowledge Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVxdWVzdA

AupAcknowledgeRequest.


# Class Name

`AupAcknowledgeRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `choice` | [`ChoiceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/choice.md) | Required | Choice. |
| `description_digest` | `str` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluation_id` | `str` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```python
from tradeglotlocalconsole.models.aup_acknowledge_request import AupAcknowledgeRequest
from tradeglotlocalconsole.models.choice_enum import ChoiceEnum

aup_acknowledge_request = AupAcknowledgeRequest(
    choice=ChoiceEnum.ACKNOWLEDGE_AND_CONTINUE,
    description_digest='description_digest2',
    evaluation_id='evaluation_id8'
)
```



