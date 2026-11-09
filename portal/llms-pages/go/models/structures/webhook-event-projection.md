# Webhook Event Projection

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRldlYmhvb2tFdmVudFByb2plY3Rpb24

All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary.


# Class Name

`WebhookEventProjection`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `EventType` | [`models.WebhookEventProjectionEventType`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-event-type.md) | Required | This is a container for any-of cases. |
| `Id` | [`models.WebhookEventProjectionId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-id.md) | Required | This is a container for any-of cases. |
| `ResourceId` | [`models.WebhookEventProjectionResourceId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-resource-id.md) | Required | This is a container for any-of cases. |
| `ResourceStatus` | [`models.WebhookEventProjectionResourceStatus`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-resource-status.md) | Required | This is a container for any-of cases. |
| `ResourceType` | [`models.WebhookEventProjectionResourceType`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-resource-type.md) | Required | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    webhookEventProjection := models.WebhookEventProjection{
        EventType:      models.WebhookEventProjectionEventTypeContainer.FromString("String9"),
        Id:             models.WebhookEventProjectionIdContainer.FromString("String9"),
        ResourceId:     models.WebhookEventProjectionResourceIdContainer.FromString("String5"),
        ResourceStatus: models.WebhookEventProjectionResourceStatusContainer.FromString("String1"),
        ResourceType:   models.WebhookEventProjectionResourceTypeContainer.FromString("String3"),
    }

}
```



