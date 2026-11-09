# Card

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkNhcmQ

Card.


# Class Name

`Card`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `brand` | str \| None | Optional | This is a container for any-of cases. |
| `category` | str \| None | Optional | This is a container for any-of cases. |
| `image_url` | str \| None | Optional | This is a container for any-of cases. |
| `key_features` | `List[str]` | Optional | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `materials` | `List[str]` | Optional | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `product_id` | `str` | Optional | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `title` | `str` | Optional | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```python
from tradeglotlocalconsole.models.card import Card

card = Card(
    brand='String1',
    category='String5',
    image_url='String3',
    key_features=[
        'key_features2'
    ],
    materials=[
        'materials7',
        'materials8',
        'materials9'
    ]
)
```



