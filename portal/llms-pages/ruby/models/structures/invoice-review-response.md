# Invoice Review Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXNwb25zZQ

InvoiceReviewResponse.


# Class Name

`InvoiceReviewResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | `String` | Required, Constant | Action.<br><br>**Value**: `'create_sandbox_invoice_draft'` |
| `advisory_only` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `authenticated_actor` | `String` | Required, Constant | Authenticated actor.<br><br>**Value**: `'False'` |
| `expires_at` | `String` | Required | Expires at. |
| `limitations` | `Array[String]` | Required | Limitations. |
| `payload_digest` | `String` | Required | Payload digest. |
| `policy_status` | `String` | Required, Constant | Policy status.<br><br>**Value**: `'manual_review'` |
| `review_token` | `String` | Required | Review token. |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |


# Example

```ruby
invoice_review_response = InvoiceReviewResponse.new(
  'create_sandbox_invoice_draft',
  'True',
  'False',
  'expires_at4',
  [
    'limitations9'
  ],
  'payload_digest2',
  'manual_review',
  'review_token0',
  'synthetic'
)
```



