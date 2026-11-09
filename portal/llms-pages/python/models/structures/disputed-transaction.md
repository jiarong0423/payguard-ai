# Disputed Transaction

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVkVHJhbnNhY3Rpb24

DisputedTransaction.


# Class Name

`DisputedTransaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `gross_amount` | [ProviderMoney](http://localhost:3000/llms-pages/python/models/structures/provider-money.md) \| None | Optional | This is a container for any-of cases. |
| `seller_protection_eligible` | bool \| None | Optional | This is a container for any-of cases. |
| `seller_transaction_id` | `str` | Required | Seller transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9._-]{1,64}$` |
| `transaction_status` | str \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.disputed_transaction import DisputedTransaction
from tradeglotlocalconsole.models.provider_money import ProviderMoney

disputed_transaction = DisputedTransaction(
    seller_transaction_id='seller_transaction_id8',
    gross_amount=ProviderMoney(
        currency_code='currency_code0',
        value='value6'
    ),
    seller_protection_eligible=True,
    transaction_status='String3'
)
```



