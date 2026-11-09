# Paypal Status Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNl

PaypalStatusResponse.


# Interface Name

`PaypalStatusResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `configured` | `boolean` | Required | Configured. |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidenceReceipt` | [`PaypalStatusResponseEvidenceReceipt`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/paypal-status-response-evidence-receipt.md) | Required | This is a container for any-of cases. |
| `lastVerifiedAt` | [`PaypalStatusResponseLastVerifiedAt`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/paypal-status-response-last-verified-at.md) | Required | This is a container for any-of cases. |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'paypal_sandbox'` |
| `status` | [`Status11Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-11.md) | Required | Status. |


# Example

```ts
import {
  ActionEnum,
  EvidenceClass3Enum,
  PaypalStatusResponse,
  Status10Enum,
  Status11Enum,
} from 'tradeglot-local-consolelib';

const paypalStatusResponse: PaypalStatusResponse = {
  configured: false,
  environment: 'sandbox',
  evidenceReceipt: {
    action: ActionEnum.OAUTHCONNECT,
    environment: 'sandbox',
    evidenceClass: EvidenceClass3Enum.AUTHENTICSANDBOXRESPONSE,
    externalSend: 'FROZEN',
    invoiceId: 'String5',
    observedAt: 'observed_at8',
    paypalDebugId: 'String5',
    proofKind: 'POST_RESPONSE_ONLY',
    schemaVersion: 1,
    separateGetReadback: 'False',
    status: Status10Enum.CONNECTED,
  },
  lastVerifiedAt: 'String3',
  source: 'paypal_sandbox',
  status: Status11Enum.Connected,
};
```



