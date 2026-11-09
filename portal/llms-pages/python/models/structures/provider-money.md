# Provider Money

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlByb3ZpZGVyTW9uZXk

ProviderMoney.


# Class Name

`ProviderMoney`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currency_code` | `str` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `str` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```python
from tradeglotlocalconsole.models.provider_money import ProviderMoney

provider_money = ProviderMoney(
    currency_code='currency_code8',
    value='value4'
)
```



