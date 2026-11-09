# Provide Evidence Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlcXVlc3Q

ProvideEvidenceRequest.


# Class Name

`ProvideEvidenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `str` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirm_token` | str \| None | Optional | This is a container for any-of cases. |
| `dispute_id` | `str` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `submit` | `bool` | Optional | Submit.<br><br>**Default**: `False` |


# Example

```python
from tradeglotlocalconsole.models.provide_evidence_request import ProvideEvidenceRequest

provide_evidence_request = ProvideEvidenceRequest(
    case_ref='case_ref8',
    dispute_id='dispute_id6',
    confirm_token='String5',
    submit=False
)
```



