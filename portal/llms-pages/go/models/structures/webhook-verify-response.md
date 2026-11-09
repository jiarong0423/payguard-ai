# Webhook Verify Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRldlYmhvb2tWZXJpZnlSZXNwb25zZQ

WebhookVerifyResponse.


# Class Name

`WebhookVerifyResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Event` | [`models.WebhookEventProjection`](http://localhost:3000/llms-pages/go/models/structures/webhook-event-projection.md) | Required | All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary. |
| `ImportedIntoDemo` | `string` | Required, Constant | Imported into demo.<br><br>**Value**: `"False"` |
| `PaypalDebugId` | [`models.WebhookVerifyResponsePaypalDebugId`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/webhook-verify-response-paypal-debug-id.md) | Required | This is a container for any-of cases. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` |
| `VerificationStatus` | `string` | Required, Constant | Verification status.<br><br>**Value**: `"SUCCESS"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    webhookVerifyResponse := models.WebhookVerifyResponse{
        Event:              models.WebhookEventProjection{
            EventType:      models.WebhookEventProjectionEventTypeContainer.FromString("String1"),
            Id:             models.WebhookEventProjectionIdContainer.FromString("String1"),
            ResourceId:     models.WebhookEventProjectionResourceIdContainer.FromString("String7"),
            ResourceStatus: models.WebhookEventProjectionResourceStatusContainer.FromString("String9"),
            ResourceType:   models.WebhookEventProjectionResourceTypeContainer.FromString("String5"),
        },
        ImportedIntoDemo:   "False",
        PaypalDebugId:      models.WebhookVerifyResponsePaypalDebugIdContainer.FromString("String9"),
        Source:             "paypal_sandbox",
        VerificationStatus: "SUCCESS",
    }

}
```



