# Product Reference Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXNwb25zZQ

Up to three Channel3 products for the seller to pick from; advisory, never changes the AUP decision.


# Class Name

`ProductReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affects_decision` | `str` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `cards` | [`List[ProductCard]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/product-card.md) | Required | Cards.<br><br>**Constraints**: *Maximum Items*: `3` |
| `reason` | [Reason7](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/reason-7.md) | Required | This is a container for any-of cases. |
| `recorded_at` | str | Required | This is a container for any-of cases. |
| `source` | [Source11](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/source-11.md) | Required | This is a container for any-of cases. |
| `status` | [`Status12Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status-12.md) | Required | Status. |


# Example

```python
from tradeglotlocalconsole.models.product_card import ProductCard
from tradeglotlocalconsole.models.product_reference_response import ProductReferenceResponse
from tradeglotlocalconsole.models.reason_7_enum import Reason7Enum
from tradeglotlocalconsole.models.source_11_enum import Source11Enum
from tradeglotlocalconsole.models.status_12_enum import Status12Enum

product_reference_response = ProductReferenceResponse(
    cards=[
        ProductCard(
            brand='String3',
            category='String7',
            image_url='String5',
            key_features=[
                'key_features4',
                'key_features5',
                'key_features6'
            ],
            materials=[
                'materials9',
                'materials0'
            ],
            product_id='product_id4',
            title='title4'
        )
    ],
    reason=Reason7Enum.BUDGET_EXHAUSTED,
    recorded_at='String5',
    source=Source11Enum.CHANNEL3_LIVE,
    status=Status12Enum.NOT_FOUND
)
```



