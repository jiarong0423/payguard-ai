# Webhook Event Projection

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRldlYmhvb2tFdmVudFByb2plY3Rpb24

All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary.


# Class Name

`WebhookEventProjection`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `EventType` | [`WebhookEventProjectionEventType`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/webhook-event-projection-event-type.md) | Required | This is a container for any-of cases. |
| `Id` | [`WebhookEventProjectionId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/webhook-event-projection-id.md) | Required | This is a container for any-of cases. |
| `ResourceId` | [`WebhookEventProjectionResourceId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/webhook-event-projection-resource-id.md) | Required | This is a container for any-of cases. |
| `ResourceStatus` | [`WebhookEventProjectionResourceStatus`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/webhook-event-projection-resource-status.md) | Required | This is a container for any-of cases. |
| `ResourceType` | [`WebhookEventProjectionResourceType`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/webhook-event-projection-resource-type.md) | Required | This is a container for any-of cases. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

WebhookEventProjection webhookEventProjection = new WebhookEventProjection
{
    EventType = WebhookEventProjectionEventType.FromString("String9"),
    Id = WebhookEventProjectionId.FromString("String9"),
    ResourceId = WebhookEventProjectionResourceId.FromString("String5"),
    ResourceStatus = WebhookEventProjectionResourceStatus.FromString("String1"),
    ResourceType = WebhookEventProjectionResourceType.FromString("String3"),
};
```



