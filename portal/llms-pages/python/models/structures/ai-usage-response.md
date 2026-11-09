# Ai Usage Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFpVXNhZ2VSZXNwb25zZQ

AiUsageResponse.


# Class Name

`AiUsageResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `content_logged` | `bool` | Optional | Content logged.<br><br>**Default**: `False` |
| `cost_note` | `str` | Required | Cost note. |
| `entries` | [`List[AiUsageEntry]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/ai-usage-entry.md) | Required | Entries.<br><br>**Constraints**: *Maximum Items*: `50` |
| `price_table_source` | `str` | Required | Price table source. |
| `source` | [`Source1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/source-1.md) | Required | Source. |


# Example

```python
from tradeglotlocalconsole.models.ai_usage_entry import AiUsageEntry
from tradeglotlocalconsole.models.ai_usage_response import AiUsageResponse
from tradeglotlocalconsole.models.outcome_enum import OutcomeEnum
from tradeglotlocalconsole.models.source_1_enum import Source1Enum
from tradeglotlocalconsole.models.stage_2_enum import Stage2Enum

ai_usage_response = AiUsageResponse(
    cost_note='cost_note2',
    entries=[
        AiUsageEntry(
            at='at6',
            latency_ms=254,
            outcome=OutcomeEnum.OK,
            stage=Stage2Enum.STUDIO_AGENT,
            estimated_cost_usd='String7',
            model='String9',
            tokens_in=196,
            tokens_out=54,
            tokens_total=118
        )
    ],
    price_table_source='price_table_source8',
    source=Source1Enum.SESSION_MEMORY,
    content_logged=False
)
```



