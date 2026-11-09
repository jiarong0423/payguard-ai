# Guide Start Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Class Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `goods_type` | [GoodsType](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/goods-type.md) \| None | Optional | This is a container for any-of cases. |
| `scenario` | [`Scenario2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/scenario-2.md) | Required | Scenario. |


# Example

```python
from tradeglotlocalconsole.models.goods_type_enum import GoodsTypeEnum
from tradeglotlocalconsole.models.guide_start_request import GuideStartRequest
from tradeglotlocalconsole.models.scenario_2_enum import Scenario2Enum

guide_start_request = GuideStartRequest(
    scenario=Scenario2Enum.DISPUTE,
    goods_type=GoodsTypeEnum.PHYSICAL
)
```



