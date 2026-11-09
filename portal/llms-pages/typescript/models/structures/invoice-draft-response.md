# Invoice Draft Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlc3BvbnNl

InvoiceDraftResponse.


# Interface Name

`InvoiceDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidenceReceipt` | [`SandboxEvidenceReceipt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/sandbox-evidence-receipt.md) | Required | SandboxEvidenceReceipt. |
| `externalSend` | `string` | Required, Constant | External send.<br><br>**Value**: `'FROZEN'` |
| `invoiceId` | `string` | Required | Invoice id.<br><br>**Constraints**: *Minimum Length*: `13`, *Maximum Length*: `69`, *Pattern*: `^INV2-[A-Z0-9-]{8,64}$` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'paypal_sandbox'` |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'DRAFT'` |


# Example

```ts
import {
  ActionEnum,
  EvidenceClass3Enum,
  InvoiceDraftResponse,
  Status10Enum,
} from 'tradeglot-local-consolelib';

const invoiceDraftResponse: InvoiceDraftResponse = {
  environment: 'sandbox',
  evidenceReceipt: {
    action: ActionEnum.OAUTHCONNECT,
    environment: 'sandbox',
    evidenceClass: EvidenceClass3Enum.AUTHENTICSANDBOXRESPONSE,
    externalSend: 'FROZEN',
    invoiceId: 'String3',
    observedAt: 'observed_at6',
    paypalDebugId: 'String3',
    proofKind: 'POST_RESPONSE_ONLY',
    schemaVersion: 1,
    separateGetReadback: 'False',
    status: Status10Enum.CONNECTED,
  },
  externalSend: 'FROZEN',
  invoiceId: 'invoice_id6',
  source: 'paypal_sandbox',
  status: 'DRAFT',
};
```



