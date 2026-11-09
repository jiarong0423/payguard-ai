# Guide Review Row

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3Um93

GuideReviewRow.


# Class Name

`GuideReviewRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `str` | Required | Item. |
| `source` | [`Source9Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/source-9.md) | Required | Source. |
| `value` | `str` | Required | Value.<br><br>**Constraints**: *Maximum Length*: `120` |


# Example

```python
from tradeglotlocalconsole.models.guide_review_row import GuideReviewRow
from tradeglotlocalconsole.models.source_9_enum import Source9Enum

guide_review_row = GuideReviewRow(
    item='item2',
    source=Source9Enum.WORDS,
    value='value2'
)
```



