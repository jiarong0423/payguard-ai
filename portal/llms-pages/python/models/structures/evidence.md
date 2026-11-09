# Evidence

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkV2aWRlbmNl

Evidence.


# Class Name

`Evidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrier_status` | str \| None | Optional | This is a container for any-of cases. |
| `delivered_at` | str \| None | Optional | This is a container for any-of cases. |
| `evidence_source` | `str` | Required, Constant | Evidence source.<br><br>**Value**: `"synthetic"` |
| `opened_at` | str \| None | Optional | This is a container for any-of cases. |
| `order_created_at` | str \| None | Optional | This is a container for any-of cases. |
| `reason` | str \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.evidence import Evidence

evidence = Evidence(
    carrier_status='String5',
    delivered_at='String1',
    opened_at='String1',
    order_created_at='String3',
    reason='String3'
)
```



