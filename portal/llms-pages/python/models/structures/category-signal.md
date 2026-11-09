# Category Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkNhdGVnb3J5U2lnbmFs

CategorySignal.


# Class Name

`CategorySignal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | str | Required | This is a container for any-of cases. |
| `confidence` | [Confidence](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/confidence.md) | Required | This is a container for any-of cases. |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"channel3"` |


# Example

```python
from tradeglotlocalconsole.models.category_signal import CategorySignal
from tradeglotlocalconsole.models.confidence_enum import ConfidenceEnum

category_signal = CategorySignal(
    category='String9',
    confidence=ConfidenceEnum.HIGH
)
```



