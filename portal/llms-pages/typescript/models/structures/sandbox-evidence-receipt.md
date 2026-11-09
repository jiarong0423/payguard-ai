# Sandbox Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlNhbmRib3hFdmlkZW5jZVJlY2VpcHQ

SandboxEvidenceReceipt.


# Interface Name

`SandboxEvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | [`ActionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/action.md) | Required | Action. |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidenceClass` | [`EvidenceClass3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/evidence-class-3.md) | Required | Evidence class. |
| `externalSend` | `string` | Required, Constant | External send.<br><br>**Value**: `'FROZEN'` |
| `invoiceId` | [`SandboxEvidenceReceiptInvoiceId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/sandbox-evidence-receipt-invoice-id.md) | Required | This is a container for any-of cases. |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypalDebugId` | [`SandboxEvidenceReceiptPaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/sandbox-evidence-receipt-paypal-debug-id.md) | Required | This is a container for any-of cases. |
| `proofKind` | `string` | Required, Constant | Proof kind.<br><br>**Value**: `'POST_RESPONSE_ONLY'` |
| `schemaVersion` | `number` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `separateGetReadback` | `string` | Required, Constant | Separate get readback.<br><br>**Value**: `'False'` |
| `status` | [`Status10Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/status-10.md) | Required | Status. |


# Example

```ts
import {
  ActionEnum,
  EvidenceClass3Enum,
  SandboxEvidenceReceipt,
  Status10Enum,
} from 'tradeglot-local-consolelib';

const sandboxEvidenceReceipt: SandboxEvidenceReceipt = {
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
};
```



