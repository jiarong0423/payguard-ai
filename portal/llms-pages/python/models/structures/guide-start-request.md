# Guide Start Request

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Class Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `goods_type` | [GoodsType](http://localhost:3000/llms-pages/python/models/enumerations/goods-type.md) \| None | Optional | This is a container for any-of cases. |
| `scenario` | [`Scenario2Enum`](http://localhost:3000/llms-pages/python/models/enumerations/scenario-2.md) | Required | Scenario. |


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



