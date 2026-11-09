# Dispute Amount

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVBbW91bnQ

Dispute amount.


# Class Name

`DisputeAmount`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currency_code` | `str` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `str` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```python
from tradeglotlocalconsole.models.dispute_amount import DisputeAmount

dispute_amount = DisputeAmount(
    currency_code='currency_code6',
    value='value0'
)
```



