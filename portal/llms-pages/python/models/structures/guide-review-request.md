# Guide Review Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3UmVxdWVzdA

GuideReviewRequest.


# Class Name

`GuideReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `change` | `List[str]` | Optional | Change.<br><br>**Constraints**: *Maximum Items*: `9`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` |
| `confirm` | `bool` | Optional | Confirm.<br><br>**Default**: `False` |
| `scenario` | [Scenario1](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/scenario-1.md) \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.guide_review_request import GuideReviewRequest
from tradeglotlocalconsole.models.scenario_1_enum import Scenario1Enum

guide_review_request = GuideReviewRequest(
    change=[
        'change1',
        'change2'
    ],
    confirm=False,
    scenario=Scenario1Enum.VELOCITY
)
```



