# Aup Category Signal Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2U

Optional Channel3 signal shown next to the AUP result; it never changes the rule decision.


# Class Name

`AupCategorySignalResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affects_decision` | `str` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `reason` | [Reason](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/reason.md) | Required | This is a container for any-of cases. |
| `signal` | [CategorySignal](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/category-signal.md) | Required | This is a container for any-of cases. |
| `status` | [`Status2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status-2.md) | Required | Status. |


# Example

```python
from tradeglotlocalconsole.models.aup_category_signal_response import AupCategorySignalResponse
from tradeglotlocalconsole.models.category_signal import CategorySignal
from tradeglotlocalconsole.models.confidence_enum import ConfidenceEnum
from tradeglotlocalconsole.models.reason_enum import ReasonEnum
from tradeglotlocalconsole.models.status_2_enum import Status2Enum

aup_category_signal_response = AupCategorySignalResponse(
    reason=ReasonEnum.TIMEOUT,
    signal=CategorySignal(
        category='String9',
        confidence=ConfidenceEnum.HIGH
    ),
    status=Status2Enum.OFF
)
```



