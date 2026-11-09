# Guide Item

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkd1aWRlSXRlbQ

GuideItem.


# Class Name

`GuideItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chunk` | str | Required | This is a container for any-of cases. |
| `form` | [GuideForm](http://localhost:3000/llms-pages/python/models/structures/guide-form.md) | Required | This is a container for any-of cases. |
| `id` | `str` | Required | Id. |
| `label` | `str` | Required | Label. |
| `source` | [`Source8Enum`](http://localhost:3000/llms-pages/python/models/enumerations/source-8.md) | Required | Source. |
| `status` | [`Status9Enum`](http://localhost:3000/llms-pages/python/models/enumerations/status-9.md) | Required | Status. |


# Example

```python
from tradeglotlocalconsole.models.guide_form import GuideForm
from tradeglotlocalconsole.models.guide_item import GuideItem
from tradeglotlocalconsole.models.guide_option import GuideOption
from tradeglotlocalconsole.models.kind_2_enum import Kind2Enum
from tradeglotlocalconsole.models.source_8_enum import Source8Enum
from tradeglotlocalconsole.models.status_9_enum import Status9Enum

guide_item = GuideItem(
    chunk='String1',
    form=GuideForm(
        kind=Kind2Enum.CHOICE,
        options=[
            GuideOption(
                label='label2',
                value='value4'
            )
        ],
        placeholder='String9'
    ),
    id='id6',
    label='label6',
    source=Source8Enum.OFFICIAL,
    status=Status9Enum.STRUCTURALLY_PRESENT
)
```



