# Document Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRvY3VtZW50UmVkYWN0aW9u

DocumentRedaction.


# Class Name

`DocumentRedaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `counts` | `Hash[String, Integer]` | Required | Counts.<br><br>**Constraints**: `>= 1`, `<= 128` |
| `export_profile` | `String` | Required, Constant | Export profile.<br><br>**Value**: `'INTERNAL_REVIEW_ONLY_V1'` |
| `limitations` | `Array[String]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `limited_detection` | `String` | Required, Constant | Limited detection.<br><br>**Value**: `'True'` |
| `manual_review_required` | `String` | Required, Constant | Manual review required.<br><br>**Value**: `'True'` |
| `method` | `String` | Required, Constant | Method.<br><br>**Value**: `'HMAC-SHA256 document pseudonymization v1'` |
| `redacted_text` | `String` | Required | Redacted text.<br><br>**Constraints**: *Maximum Length*: `32768` |
| `replacement_count` | `Integer` | Required | Replacement count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `reversibility` | `String` | Required, Constant | Reversibility.<br><br>**Value**: `'False'` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `types` | [`Array[TypeEnum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/type.md) | Required | Types.<br><br>**Constraints**: *Maximum Items*: `7` |


# Example

```ruby
document_redaction = DocumentRedaction.new(
  {
    'key0': 128
  },
  'INTERNAL_REVIEW_ONLY_V1',
  [
    'limitations9',
    'limitations8',
    'limitations7'
  ],
  'True',
  'True',
  'HMAC-SHA256 document pseudonymization v1',
  'redacted_text8',
  128,
  'False',
  'synthetic',
  [
    TypeEnum::MANUAL
  ]
)
```



