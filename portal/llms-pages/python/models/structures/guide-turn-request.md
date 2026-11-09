# Guide Turn Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3Q

GuideTurnRequest.


# Class Name

`GuideTurnRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `fields` | List[[GuideField](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/guide-field.md)] \| None | Optional | This is a container for any-of cases. |
| `scenario` | [Scenario1](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/scenario-1.md) \| None | Optional | This is a container for any-of cases. |
| `text` | `str` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1600` |


# Example

```python
from tradeglotlocalconsole.models.guide_field import GuideField
from tradeglotlocalconsole.models.guide_turn_request import GuideTurnRequest
from tradeglotlocalconsole.models.scenario_1_enum import Scenario1Enum

guide_turn_request = GuideTurnRequest(
    text='text0',
    fields=[
        GuideField(
            item='item8',
            value='value8'
        ),
        GuideField(
            item='item8',
            value='value8'
        ),
        GuideField(
            item='item8',
            value='value8'
        )
    ],
    scenario=Scenario1Enum.DISPUTE
)
```



