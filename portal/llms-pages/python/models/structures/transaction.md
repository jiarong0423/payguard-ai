# Transaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlRyYW5zYWN0aW9u

Transaction.


# Class Name

`Transaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `amount` | `str` | Required | Amount. |
| `currency` | `str` | Required | Currency. |
| `occurred_at` | `str` | Required | Occurred at. |
| `order_id` | `str` | Required | Order id. |


# Example

```python
from tradeglotlocalconsole.models.transaction import Transaction

transaction = Transaction(
    amount='amount0',
    currency='currency8',
    occurred_at='occurred_at2',
    order_id='order_id2'
)
```



