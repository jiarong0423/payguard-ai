# Dispute Evidence Row

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVFdmlkZW5jZVJvdw

DisputeEvidenceRow.


# Class Name

`DisputeEvidenceRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | str \| None | Optional | This is a container for any-of cases. |
| `date` | str \| None | Optional | This is a container for any-of cases. |
| `evidence_type` | `str` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `source` | [`Source3Enum`](http://localhost:3000/llms-pages/python/models/enumerations/source-3.md) | Required | Source. |


# Example

```python
from tradeglotlocalconsole.models.dispute_evidence_row import DisputeEvidenceRow
from tradeglotlocalconsole.models.source_3_enum import Source3Enum

dispute_evidence_row = DisputeEvidenceRow(
    evidence_type='evidence_type8',
    source=Source3Enum.REQUESTED_FROM_SELLER,
    action='String7',
    date='String3'
)
```



