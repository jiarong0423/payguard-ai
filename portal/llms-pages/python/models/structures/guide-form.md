# Guide Form

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkd1aWRlRm9ybQ

GuideForm.


# Class Name

`GuideForm`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `kind` | [`Kind2Enum`](http://localhost:3000/llms-pages/python/models/enumerations/kind-2.md) | Required | Kind. |
| `options` | [`List[GuideOption]`](http://localhost:3000/llms-pages/python/models/structures/guide-option.md) | Required | Options. |
| `placeholder` | str | Required | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.guide_form import GuideForm
from tradeglotlocalconsole.models.guide_option import GuideOption
from tradeglotlocalconsole.models.kind_2_enum import Kind2Enum

guide_form = GuideForm(
    kind=Kind2Enum.TEXT,
    options=[
        GuideOption(
            label='label2',
            value='value4'
        )
    ],
    placeholder='String7'
)
```



