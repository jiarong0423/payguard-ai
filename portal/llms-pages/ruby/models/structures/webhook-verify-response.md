# Webhook Verify Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRldlYmhvb2tWZXJpZnlSZXNwb25zZQ

WebhookVerifyResponse.


# Class Name

`WebhookVerifyResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `event` | [`WebhookEventProjection`](http://localhost:3000/llms-pages/ruby/models/structures/webhook-event-projection.md) | Required | All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary. |
| `imported_into_demo` | `String` | Required, Constant | Imported into demo.<br><br>**Value**: `'False'` |
| `paypal_debug_id` | String | Required | This is a container for any-of cases. |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'paypal_sandbox'` |
| `verification_status` | `String` | Required, Constant | Verification status.<br><br>**Value**: `'SUCCESS'` |


# Example

```ruby
webhook_verify_response = WebhookVerifyResponse.new(
  WebhookEventProjection.new(
    'String1',
    'String1',
    'String7',
    'String9',
    'String5'
  ),
  'False',
  'String9',
  'paypal_sandbox',
  'SUCCESS'
)
```



