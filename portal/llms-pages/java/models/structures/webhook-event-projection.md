# Webhook Event Projection

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRldlYmhvb2tFdmVudFByb2plY3Rpb24

All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary.


# Class Name

`WebhookEventProjection`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `EventType` | [`WebhookEventProjectionEventType`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/webhook-event-projection-event-type.md) | Required | This is a container for any-of cases. | WebhookEventProjectionEventType getEventType() | setEventType(WebhookEventProjectionEventType eventType) |
| `Id` | [`WebhookEventProjectionId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/webhook-event-projection-id.md) | Required | This is a container for any-of cases. | WebhookEventProjectionId getId() | setId(WebhookEventProjectionId id) |
| `ResourceId` | [`WebhookEventProjectionResourceId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/webhook-event-projection-resource-id.md) | Required | This is a container for any-of cases. | WebhookEventProjectionResourceId getResourceId() | setResourceId(WebhookEventProjectionResourceId resourceId) |
| `ResourceStatus` | [`WebhookEventProjectionResourceStatus`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/webhook-event-projection-resource-status.md) | Required | This is a container for any-of cases. | WebhookEventProjectionResourceStatus getResourceStatus() | setResourceStatus(WebhookEventProjectionResourceStatus resourceStatus) |
| `ResourceType` | [`WebhookEventProjectionResourceType`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/webhook-event-projection-resource-type.md) | Required | This is a container for any-of cases. | WebhookEventProjectionResourceType getResourceType() | setResourceType(WebhookEventProjectionResourceType resourceType) |


# Example

```java
import m18000.m0.m0.m127.models.WebhookEventProjection;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionEventType;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionId;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionResourceId;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionResourceStatus;
import m18000.m0.m0.m127.models.containers.WebhookEventProjectionResourceType;

WebhookEventProjection webhookEventProjection = new WebhookEventProjection.Builder(
    WebhookEventProjectionEventType.fromString(
        "String9"
    ),
    WebhookEventProjectionId.fromString(
        "String9"
    ),
    WebhookEventProjectionResourceId.fromString(
        "String5"
    ),
    WebhookEventProjectionResourceStatus.fromString(
        "String1"
    ),
    WebhookEventProjectionResourceType.fromString(
        "String3"
    )
)
.build();
```



