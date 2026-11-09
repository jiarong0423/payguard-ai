# Webhook Event Projection

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRldlYmhvb2tFdmVudFByb2plY3Rpb24

All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary.


# Class Name

`WebhookEventProjection`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `EventType` | [`models.WebhookEventProjectionEventType`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-event-type.md) | Required | This is a container for any-of cases. |
| `Id` | [`models.WebhookEventProjectionId`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-id.md) | Required | This is a container for any-of cases. |
| `ResourceId` | [`models.WebhookEventProjectionResourceId`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-resource-id.md) | Required | This is a container for any-of cases. |
| `ResourceStatus` | [`models.WebhookEventProjectionResourceStatus`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-resource-status.md) | Required | This is a container for any-of cases. |
| `ResourceType` | [`models.WebhookEventProjectionResourceType`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/webhook-event-projection-resource-type.md) | Required | This is a container for any-of cases. |


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



