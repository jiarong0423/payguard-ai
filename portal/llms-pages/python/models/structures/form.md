# Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkZvcm0

Form.


# Class Name

`Form`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `kind` | [`Kind2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/kind-2.md) | Optional | Kind. |
| `options` | [`List[GuideOption]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/guide-option.md) | Optional | Options. |
| `placeholder` | str \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.form import Form
from tradeglotlocalconsole.models.guide_option import GuideOption
from tradeglotlocalconsole.models.kind_2_enum import Kind2Enum

form = Form(
    kind=Kind2Enum.TEXT,
    options=[
        GuideOption(
            label='label2',
            value='value4'
        ),
        GuideOption(
            label='label2',
            value='value4'
        ),
        GuideOption(
            label='label2',
            value='value4'
        )
    ],
    placeholder='String9'
)
```



