# Webhook Verify Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRldlYmhvb2tWZXJpZnlSZXNwb25zZQ

WebhookVerifyResponse.


# Class Name

`WebhookVerifyResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `event` | [`WebhookEventProjection`](http://localhost:3000/llms-pages/php/models/structures/webhook-event-projection.md) | Required | All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary. | getEvent(): WebhookEventProjection | setEvent(WebhookEventProjection event): void |
| `importedIntoDemo` | `string` | Required, Constant | Imported into demo.<br><br>**Value**: `'False'` | getImportedIntoDemo(): string | setImportedIntoDemo(string importedIntoDemo): void |
| `paypalDebugId` | string | Required | This is a container for any-of cases. | getPaypalDebugId(): string | setPaypalDebugId(string paypalDebugId): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'paypal_sandbox'` | getSource(): string | setSource(string source): void |
| `verificationStatus` | `string` | Required, Constant | Verification status.<br><br>**Value**: `'SUCCESS'` | getVerificationStatus(): string | setVerificationStatus(string verificationStatus): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\WebhookVerifyResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\WebhookEventProjectionBuilder;

$webhookVerifyResponse = WebhookVerifyResponseBuilder::init(
    WebhookEventProjectionBuilder::init(
        'String1',
        'String1',
        'String7',
        'String9',
        'String5'
    )->build(),
    'String9'
)->build();
```



