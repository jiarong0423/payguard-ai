# Product Card

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlByb2R1Y3RDYXJk

A Channel3 catalogue product reduced to what identifies the item; no prices, offers or buy links.


# Class Name

`ProductCard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `brand` | str | Required | This is a container for any-of cases. |
| `category` | str | Required | This is a container for any-of cases. |
| `image_url` | str | Required | This is a container for any-of cases. |
| `key_features` | `List[str]` | Required | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `materials` | `List[str]` | Required | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `product_id` | `str` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `title` | `str` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```python
from tradeglotlocalconsole.models.product_card import ProductCard

product_card = ProductCard(
    brand='String3',
    category='String7',
    image_url='String5',
    key_features=[
        'key_features4'
    ],
    materials=[
        'materials9',
        'materials0',
        'materials1'
    ],
    product_id='product_id4',
    title='title4'
)
```



