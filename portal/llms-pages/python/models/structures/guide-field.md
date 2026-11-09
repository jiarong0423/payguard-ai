# Guide Field

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkd1aWRlRmllbGQ

GuideField.


# Class Name

`GuideField`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `str` | Required | Item.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` |
| `value` | `str` | Required | Value.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `120` |


# Example

```python
from tradeglotlocalconsole.models.guide_field import GuideField

guide_field = GuideField(
    item='item4',
    value='value4'
)
```



