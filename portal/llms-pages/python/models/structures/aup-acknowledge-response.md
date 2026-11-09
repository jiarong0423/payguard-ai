# Aup Acknowledge Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVzcG9uc2U

AupAcknowledgeResponse.


# Class Name

`AupAcknowledgeResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `acknowledgement_token` | str | Required | This is a container for any-of cases. |
| `choice` | [`ChoiceEnum`](http://localhost:3000/llms-pages/python/models/enumerations/choice.md) | Required | Choice. |
| `compliance_decision` | `str` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` |
| `description_digest` | `str` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluation_id` | `str` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `expires_at` | str | Required | This is a container for any-of cases. |
| `external_action_authorized` | `str` | Required, Constant | External action authorized.<br><br>**Value**: `"False"` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `warning_copy_version` | `str` | Required, Constant | Warning copy version.<br><br>**Value**: `"aup-warning-v1"` |


# Example

```python
from tradeglotlocalconsole.models.aup_acknowledge_response import AupAcknowledgeResponse
from tradeglotlocalconsole.models.choice_enum import ChoiceEnum

aup_acknowledge_response = AupAcknowledgeResponse(
    acknowledgement_token='String1',
    choice=ChoiceEnum.ACKNOWLEDGE_AND_CONTINUE,
    description_digest='description_digest8',
    evaluation_id='evaluation_id4',
    expires_at='String7'
)
```



