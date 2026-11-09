# Gross Amount

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkdyb3NzQW1vdW50

Gross amount.


# Class Name

`GrossAmount`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currency_code` | `str` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `str` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```python
from tradeglotlocalconsole.models.gross_amount import GrossAmount

gross_amount = GrossAmount(
    currency_code='currency_code4',
    value='value0'
)
```



