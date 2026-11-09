# Signal

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | str \| None | Optional | This is a container for any-of cases. |
| `confidence` | [Confidence](http://localhost:3000/llms-pages/python/models/enumerations/confidence.md) \| None | Optional | This is a container for any-of cases. |
| `source` | [`Source2Enum`](http://localhost:3000/llms-pages/python/models/enumerations/source-2.md) | Optional | Source. |


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



