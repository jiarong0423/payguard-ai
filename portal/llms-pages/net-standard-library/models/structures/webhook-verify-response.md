# Webhook Verify Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRldlYmhvb2tWZXJpZnlSZXNwb25zZQ

WebhookVerifyResponse.


# Class Name

`WebhookVerifyResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Event` | [`WebhookEventProjection`](http://localhost:3000/llms-pages/net-standard-library/models/structures/webhook-event-projection.md) | Required | All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary. |
| `ImportedIntoDemo` | `string` | Required, Constant | Imported into demo.<br><br>**Value**: `"False"` |
| `PaypalDebugId` | [`WebhookVerifyResponsePaypalDebugId`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/webhook-verify-response-paypal-debug-id.md) | Required | This is a container for any-of cases. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` |
| `VerificationStatus` | `string` | Required, Constant | Verification status.<br><br>**Value**: `"SUCCESS"` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

WebhookVerifyResponse webhookVerifyResponse = new WebhookVerifyResponse
{
    MEvent = new WebhookEventProjection
    {
        EventType = WebhookEventProjectionEventType.FromString("String1"),
        Id = WebhookEventProjectionId.FromString("String1"),
        ResourceId = WebhookEventProjectionResourceId.FromString("String7"),
        ResourceStatus = WebhookEventProjectionResourceStatus.FromString("String9"),
        ResourceType = WebhookEventProjectionResourceType.FromString("String5"),
    },
    ImportedIntoDemo = "False",
    PaypalDebugId = WebhookVerifyResponsePaypalDebugId.FromString("String9"),
    Source = "paypal_sandbox",
    VerificationStatus = "SUCCESS",
};
```



