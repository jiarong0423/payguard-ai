# Invoice Draft Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlcXVlc3Q

InvoiceDraftRequest.


# Class Name

`InvoiceDraftRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `amount` | `String` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` |
| `currency` | [`CurrencyEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/currency.md) | Required | Currency. |
| `description` | `String` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |
| `payload_digest` | `String` | Required | Payload digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `review_token` | `String` | Required | Review token.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128` |


# Example

```ruby
invoice_draft_request = InvoiceDraftRequest.new(
  'amount4',
  CurrencyEnum::JPY,
  'description2',
  'payload_digest2',
  'review_token0'
)
```



