# Guide Gap

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkd1aWRlR2Fw

GuideGap.


# Class Name

`GuideGap`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `conflicting` | `List[str]` | Required | Conflicting. |
| `missing` | `List[str]` | Required | Missing. |
| `partial` | `List[str]` | Required | Partial. |
| `present` | `List[str]` | Required | Present. |


# Example

```python
from tradeglotlocalconsole.models.guide_gap import GuideGap

guide_gap = GuideGap(
    conflicting=[
        'conflicting9',
        'conflicting8',
        'conflicting7'
    ],
    missing=[
        'missing2',
        'missing3'
    ],
    partial=[
        'partial4'
    ],
    present=[
        'present7'
    ]
)
```



