# Time Gaps

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlRpbWVHYXBz

TimeGaps.


# Class Name

`TimeGaps`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `delivery_to_claim` | int | Required | This is a container for any-of cases. |
| `payment_to_claim` | int | Required | This is a container for any-of cases. |
| `payment_to_delivery` | int | Required | This is a container for any-of cases. |
| `payment_to_order_record` | int | Required | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.time_gaps import TimeGaps

time_gaps = TimeGaps(
    delivery_to_claim=88,
    payment_to_claim=20,
    payment_to_delivery=30,
    payment_to_order_record=74
)
```



