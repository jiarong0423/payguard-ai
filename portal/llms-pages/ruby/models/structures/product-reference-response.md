# Product Reference Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXNwb25zZQ

Up to three Channel3 products for the seller to pick from; advisory, never changes the AUP decision.


# Class Name

`ProductReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affects_decision` | `String` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` |
| `cards` | [`Array[ProductCard]`](http://localhost:3000/llms-pages/ruby/models/structures/product-card.md) | Required | Cards.<br><br>**Constraints**: *Maximum Items*: `3` |
| `reason` | [Reason7](http://localhost:3000/llms-pages/ruby/models/enumerations/reason-7.md) | Required | This is a container for any-of cases. |
| `recorded_at` | String | Required | This is a container for any-of cases. |
| `source` | [Source11](http://localhost:3000/llms-pages/ruby/models/enumerations/source-11.md) | Required | This is a container for any-of cases. |
| `status` | [`Status12Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-12.md) | Required | Status. |


# Example

```ruby
product_reference_response = ProductReferenceResponse.new(
  'False',
  [
    ProductCard.new(
      'String3',
      'String7',
      'String5',
      [
        'key_features4',
        'key_features5',
        'key_features6'
      ],
      [
        'materials9',
        'materials0'
      ],
      'product_id4',
      'title4'
    )
  ],
  Reason7Enum::BUDGET_EXHAUSTED,
  'String5',
  Source11Enum::CHANNEL3_LIVE,
  Status12Enum::NOT_FOUND
)
```



