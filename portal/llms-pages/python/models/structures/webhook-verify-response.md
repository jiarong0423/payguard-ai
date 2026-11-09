# Webhook Verify Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRldlYmhvb2tWZXJpZnlSZXNwb25zZQ

WebhookVerifyResponse.


# Class Name

`WebhookVerifyResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `event` | [`WebhookEventProjection`](http://localhost:3000/llms-pages/python/models/structures/webhook-event-projection.md) | Required | All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary. |
| `imported_into_demo` | `str` | Required, Constant | Imported into demo.<br><br>**Value**: `"False"` |
| `paypal_debug_id` | str | Required | This is a container for any-of cases. |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` |
| `verification_status` | `str` | Required, Constant | Verification status.<br><br>**Value**: `"SUCCESS"` |


# Example

```python
from tradeglotlocalconsole.models.webhook_event_projection import WebhookEventProjection
from tradeglotlocalconsole.models.webhook_verify_response import WebhookVerifyResponse

webhook_verify_response = WebhookVerifyResponse(
    event=WebhookEventProjection(
        event_type='String1',
        id='String1',
        resource_id='String7',
        resource_status='String9',
        resource_type='String5'
    ),
    paypal_debug_id='String9'
)
```



