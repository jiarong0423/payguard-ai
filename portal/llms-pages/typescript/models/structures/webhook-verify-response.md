# Webhook Verify Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRldlYmhvb2tWZXJpZnlSZXNwb25zZQ

WebhookVerifyResponse.


# Interface Name

`WebhookVerifyResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `event` | [`WebhookEventProjection`](http://localhost:3000/llms-pages/typescript/models/structures/webhook-event-projection.md) | Required | All that is kept after a SUCCESS: identifiers and status only, no amounts, payer data, links or summary. |
| `importedIntoDemo` | `string` | Required, Constant | Imported into demo.<br><br>**Value**: `'False'` |
| `paypalDebugId` | [`WebhookVerifyResponsePaypalDebugId`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/webhook-verify-response-paypal-debug-id.md) | Required | This is a container for any-of cases. |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'paypal_sandbox'` |
| `verificationStatus` | `string` | Required, Constant | Verification status.<br><br>**Value**: `'SUCCESS'` |


# Example

```ts
import { WebhookVerifyResponse } from 'tradeglot-local-consolelib';

const webhookVerifyResponse: WebhookVerifyResponse = {
  event: {
    eventType: 'String1',
    id: 'String1',
    resourceId: 'String7',
    resourceStatus: 'String9',
    resourceType: 'String5',
  },
  importedIntoDemo: 'False',
  paypalDebugId: 'String9',
  source: 'paypal_sandbox',
  verificationStatus: 'SUCCESS',
};
```



