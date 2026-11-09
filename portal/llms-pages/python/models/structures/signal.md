# Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | str \| None | Optional | This is a container for any-of cases. |
| `confidence` | [Confidence](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/confidence.md) \| None | Optional | This is a container for any-of cases. |
| `source` | [`Source2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/source-2.md) | Optional | Source. |


# Example

```python
from tradeglotlocalconsole.models.confidence_enum import ConfidenceEnum
from tradeglotlocalconsole.models.signal import Signal
from tradeglotlocalconsole.models.source_2_enum import Source2Enum

signal = Signal(
    category='String1',
    confidence=ConfidenceEnum.HIGH,
    source=Source2Enum.CHANNEL3
)
```



