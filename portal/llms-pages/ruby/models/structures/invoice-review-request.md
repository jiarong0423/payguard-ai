# Invoice Review Request

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXF1ZXN0

InvoiceReviewRequest.


# Class Name

`InvoiceReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `acknowledgement_token` | String \| nil | Optional | This is a container for any-of cases. |
| `amount` | `String` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` |
| `confirm_sandbox_draft` | `TrueClass \| FalseClass` | Required | Confirm sandbox draft. |
| `currency` | [`CurrencyEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/currency.md) | Required | Currency. |
| `description` | `String` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |
| `description_digest` | String \| nil | Optional | This is a container for any-of cases. |
| `evaluation_id` | String \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
invoice_review_request = InvoiceReviewRequest.new(
  'amount8',
  false,
  CurrencyEnum::JPY,
  'description0',
  'String1',
  'String9',
  'String7'
)
```



