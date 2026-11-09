# Dispute Record

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVSZWNvcmQ

DisputeRecord.


# Class Name

`DisputeRecord`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `create_time` | `str` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `dispute_amount` | [`ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/provider-money.md) | Required | ProviderMoney. |
| `dispute_id` | `str` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `dispute_life_cycle_stage` | [`DisputeLifeCycleStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `dispute_state` | str \| None | Optional | This is a container for any-of cases. |
| `reason` | [`Reason2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/reason-2.md) | Required | Reason. |
| `seller_response_due_date` | str \| None | Optional | This is a container for any-of cases. |
| `status` | [`Status3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status-3.md) | Required | Status. |
| `update_time` | str \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.dispute_life_cycle_stage_enum import DisputeLifeCycleStageEnum
from tradeglotlocalconsole.models.dispute_record import DisputeRecord
from tradeglotlocalconsole.models.provider_money import ProviderMoney
from tradeglotlocalconsole.models.reason_2_enum import Reason2Enum
from tradeglotlocalconsole.models.status_3_enum import Status3Enum

dispute_record = DisputeRecord(
    create_time='create_time6',
    dispute_amount=ProviderMoney(
        currency_code='currency_code6',
        value='value0'
    ),
    dispute_id='dispute_id2',
    dispute_life_cycle_stage=DisputeLifeCycleStageEnum.UNKNOWN,
    reason=Reason2Enum.INCORRECT_AMOUNT,
    status=Status3Enum.CLOSED,
    dispute_state='String9',
    seller_response_due_date='String9',
    update_time='String9'
)
```



