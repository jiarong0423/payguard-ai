# Generated Brief

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkdlbmVyYXRlZEJyaWVm

GeneratedBrief.


# Class Name

`GeneratedBrief`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `citation_ids` | `List[str]` | Required | Citation ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3`, *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z0-9-]+$` |
| `evidence_points` | `List[str]` | Required | Evidence points.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `missing_evidence` | `List[str]` | Required | Missing evidence.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `summary` | `str` | Required | Summary.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1200` |


# Example

```python
from tradeglotlocalconsole.models.generated_brief import GeneratedBrief

generated_brief = GeneratedBrief(
    citation_ids=[
        'citation_ids5',
        'citation_ids6'
    ],
    evidence_points=[
        'evidence_points6'
    ],
    missing_evidence=[
        'missing_evidence9',
        'missing_evidence0',
        'missing_evidence1'
    ],
    summary='summary6'
)
```



