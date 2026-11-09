# Guide Form Request

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3Q

One field ({item, value}) or one round of up to three fields ({fields: [...]}), never both.


# Class Name

`GuideFormRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `confirm_review` | `bool` | Optional | Confirm review.<br><br>**Default**: `False` |
| `fields` | List[[GuideField](http://localhost:3000/llms-pages/python/models/structures/guide-field.md)] \| None | Optional | This is a container for any-of cases. |
| `item` | str \| None | Optional | This is a container for any-of cases. |
| `scenario` | [Scenario1](http://localhost:3000/llms-pages/python/models/enumerations/scenario-1.md) \| None | Optional | This is a container for any-of cases. |
| `value` | str \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.guide_field import GuideField
from tradeglotlocalconsole.models.guide_form_request import GuideFormRequest
from tradeglotlocalconsole.models.scenario_1_enum import Scenario1Enum

guide_form_request = GuideFormRequest(
    confirm_review=False,
    fields=[
        GuideField(
            item='item8',
            value='value8'
        )
    ],
    item='String9',
    scenario=Scenario1Enum.PREFLIGHT,
    value='String9'
)
```



