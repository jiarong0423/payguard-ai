# Webhook Event Projection

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRldlYmhvb2tFdmVudFByb2plY3Rpb24

All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary.


# Class Name

`WebhookEventProjection`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `eventType` | string | Required | This is a container for any-of cases. | getEventType(): string | setEventType(string eventType): void |
| `id` | string | Required | This is a container for any-of cases. | getId(): string | setId(string id): void |
| `resourceId` | string | Required | This is a container for any-of cases. | getResourceId(): string | setResourceId(string resourceId): void |
| `resourceStatus` | string | Required | This is a container for any-of cases. | getResourceStatus(): string | setResourceStatus(string resourceStatus): void |
| `resourceType` | string | Required | This is a container for any-of cases. | getResourceType(): string | setResourceType(string resourceType): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\WebhookEventProjectionBuilder;

$webhookEventProjection = WebhookEventProjectionBuilder::init(
    'String9',
    'String9',
    'String5',
    'String1',
    'String3'
)->build();
```



