# Product Confirm Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2U

The seller's own choice: one of the cards they were shown, or none of them.


# Class Name

`ProductConfirmResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affects_decision` | `String` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` |
| `card` | [ProductCard](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/product-card.md) | Required | This is a container for any-of cases. |
| `card_digest` | String | Required | This is a container for any-of cases. |
| `choice` | [`Choice2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/choice-2.md) | Required | Choice. |
| `confirmed_by` | `String` | Required, Constant | Confirmed by.<br><br>**Value**: `'seller'` |
| `description_digest` | `String` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluation_id` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `recorded_at` | String | Required | This is a container for any-of cases. |
| `source` | [`Source10Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source-10.md) | Required | Source. |


# Example

```ruby
product_confirm_response = ProductConfirmResponse.new(
  'False',
  ProductCard.new(
    'String9',
    'String3',
    'String1',
    [
      'key_features0',
      'key_features1',
      'key_features2'
    ],
    [
      'materials5',
      'materials6'
    ],
    'product_id0',
    'title0'
  ),
  'String7',
  Choice2Enum::CONFIRMED,
  'seller',
  'description_digest8',
  'evaluation_id4',
  'String5',
  Source10Enum::CHANNEL3_LIVE
)
```



