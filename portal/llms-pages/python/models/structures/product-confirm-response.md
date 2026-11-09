# Product Confirm Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2U

The seller's own choice: one of the cards they were shown, or none of them.


# Class Name

`ProductConfirmResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affects_decision` | `str` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `card` | [ProductCard](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/product-card.md) | Required | This is a container for any-of cases. |
| `card_digest` | str | Required | This is a container for any-of cases. |
| `choice` | [`Choice2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/choice-2.md) | Required | Choice. |
| `confirmed_by` | `str` | Required, Constant | Confirmed by.<br><br>**Value**: `"seller"` |
| `description_digest` | `str` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluation_id` | `str` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `recorded_at` | str | Required | This is a container for any-of cases. |
| `source` | [`Source10Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/source-10.md) | Required | Source. |


# Example

```python
from tradeglotlocalconsole.models.choice_2_enum import Choice2Enum
from tradeglotlocalconsole.models.product_card import ProductCard
from tradeglotlocalconsole.models.product_confirm_response import ProductConfirmResponse
from tradeglotlocalconsole.models.source_10_enum import Source10Enum

product_confirm_response = ProductConfirmResponse(
    card=ProductCard(
        brand='String9',
        category='String3',
        image_url='String1',
        key_features=[
            'key_features0',
            'key_features1',
            'key_features2'
        ],
        materials=[
            'materials5',
            'materials6'
        ],
        product_id='product_id0',
        title='title0'
    ),
    card_digest='String7',
    choice=Choice2Enum.CONFIRMED,
    description_digest='description_digest8',
    evaluation_id='evaluation_id4',
    recorded_at='String5',
    source=Source10Enum.CHANNEL3_LIVE
)
```



