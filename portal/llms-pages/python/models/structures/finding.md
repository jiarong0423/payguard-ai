# Finding

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkZpbmRpbmc

Finding.


# Class Name

`Finding`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | [`CategoryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/category.md) | Required | Category. |
| `code` | `str` | Required, Constant | Code.<br><br>**Value**: `"keyword_requires_policy_review"` |


# Example

```python
from tradeglotlocalconsole.models.category_enum import CategoryEnum
from tradeglotlocalconsole.models.finding import Finding

finding = Finding(
    category=CategoryEnum.UNSUPPORTED_FINANCIAL_PROMISE
)
```



