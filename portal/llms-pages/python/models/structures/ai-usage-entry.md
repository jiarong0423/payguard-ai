# Ai Usage Entry

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkFpVXNhZ2VFbnRyeQ

AiUsageEntry.


# Class Name

`AiUsageEntry`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `str` | Required | At. |
| `estimated_cost_usd` | str \| None | Optional | This is a container for any-of cases. |
| `latency_ms` | `int` | Required | Latency ms.<br><br>**Constraints**: `>= 0`, `<= 3600000` |
| `model` | str \| None | Optional | This is a container for any-of cases. |
| `outcome` | [`OutcomeEnum`](http://localhost:3000/llms-pages/python/models/enumerations/outcome.md) | Required | Outcome. |
| `stage` | [`Stage2Enum`](http://localhost:3000/llms-pages/python/models/enumerations/stage-2.md) | Required | Stage. |
| `tokens_in` | int \| None | Optional | This is a container for any-of cases. |
| `tokens_out` | int \| None | Optional | This is a container for any-of cases. |
| `tokens_total` | int \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.ai_usage_entry import AiUsageEntry
from tradeglotlocalconsole.models.outcome_enum import OutcomeEnum
from tradeglotlocalconsole.models.stage_2_enum import Stage2Enum

ai_usage_entry = AiUsageEntry(
    at='at8',
    latency_ms=36,
    outcome=OutcomeEnum.OK,
    stage=Stage2Enum.DISPUTE_MEDIATION,
    estimated_cost_usd='String9',
    model='String1',
    tokens_in=234,
    tokens_out=92,
    tokens_total=156
)
```



