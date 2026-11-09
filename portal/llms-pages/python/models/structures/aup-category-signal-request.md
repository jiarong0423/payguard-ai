# Aup Category Signal Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVxdWVzdA

AupCategorySignalRequest.


# Class Name

`AupCategorySignalRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `description` | `str` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `evaluation_id` | `str` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```python
from tradeglotlocalconsole.models.aup_category_signal_request import AupCategorySignalRequest

aup_category_signal_request = AupCategorySignalRequest(
    description='description4',
    evaluation_id='evaluation_id8'
)
```



