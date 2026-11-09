# Webhook Event Projection

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRldlYmhvb2tFdmVudFByb2plY3Rpb24

All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary.


# Interface Name

`WebhookEventProjection`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `eventType` | [`WebhookEventProjectionEventType`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/webhook-event-projection-event-type.md) | Required | This is a container for any-of cases. |
| `id` | [`WebhookEventProjectionId`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/webhook-event-projection-id.md) | Required | This is a container for any-of cases. |
| `resourceId` | [`WebhookEventProjectionResourceId`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/webhook-event-projection-resource-id.md) | Required | This is a container for any-of cases. |
| `resourceStatus` | [`WebhookEventProjectionResourceStatus`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/webhook-event-projection-resource-status.md) | Required | This is a container for any-of cases. |
| `resourceType` | [`WebhookEventProjectionResourceType`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/webhook-event-projection-resource-type.md) | Required | This is a container for any-of cases. |


# Example

```ts
import { WebhookEventProjection } from 'tradeglot-local-consolelib';

const webhookEventProjection: WebhookEventProjection = {
  eventType: 'String9',
  id: 'String9',
  resourceId: 'String5',
  resourceStatus: 'String1',
  resourceType: 'String3',
};
```



