# Add Tracking Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVxdWVzdA

AddTrackingRequest.


# Class Name

`AddTrackingRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `str` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirm_token` | str \| None | Optional | This is a container for any-of cases. |
| `dispute_id` | `str` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `submit` | `bool` | Optional | Submit.<br><br>**Default**: `False` |


# Example

```python
from tradeglotlocalconsole.models.add_tracking_request import AddTrackingRequest

add_tracking_request = AddTrackingRequest(
    case_ref='case_ref8',
    dispute_id='dispute_id6',
    confirm_token='String5',
    submit=False
)
```



