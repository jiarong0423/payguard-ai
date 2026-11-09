# Product Confirm Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVxdWVzdA

ProductConfirmRequest.


# Class Name

`ProductConfirmRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `description` | `str` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `evaluation_id` | `str` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `product_id` | str | Required | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.product_confirm_request import ProductConfirmRequest

product_confirm_request = ProductConfirmRequest(
    description='description4',
    evaluation_id='evaluation_id8',
    product_id='String1'
)
```



