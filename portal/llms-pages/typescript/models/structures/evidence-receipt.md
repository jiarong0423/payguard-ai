# Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkV2aWRlbmNlUmVjZWlwdA

Evidence receipt.


# Interface Name

`EvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | [`ActionEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/action.md) | Optional | Action. |
| `environment` | [`EnvironmentEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/environment.md) | Optional | Environment. |
| `evidenceClass` | [`EvidenceClass3Enum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/evidence-class-3.md) | Optional | Evidence class. |
| `externalSend` | [`ExternalSend1Enum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/external-send-1.md) | Optional | External send. |
| `invoiceId` | [`EvidenceReceiptInvoiceId \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/evidence-receipt-invoice-id.md) | Optional | This is a container for any-of cases. |
| `observedAt` | `string \| undefined` | Optional | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypalDebugId` | [`EvidenceReceiptPaypalDebugId \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/evidence-receipt-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `proofKind` | [`ProofKindEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/proof-kind.md) | Optional | Proof kind. |
| `schemaVersion` | [`SchemaVersion1Enum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/schema-version-1.md) | Optional | Schema version. |
| `separateGetReadback` | `boolean \| undefined` | Optional | Separate get readback. |
| `status` | [`Status10Enum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/status-10.md) | Optional | Status. |


# Example

```ts
import {
  ActionEnum,
  EnvironmentEnum,
  EvidenceClass3Enum,
  EvidenceReceipt,
  ExternalSend1Enum,
} from 'tradeglot-local-consolelib';

const evidenceReceipt: EvidenceReceipt = {
  action: ActionEnum.OAUTHCONNECT,
  environment: EnvironmentEnum.Sandbox,
  evidenceClass: EvidenceClass3Enum.AUTHENTICSANDBOXRESPONSE,
  externalSend: ExternalSend1Enum.FROZEN,
  invoiceId: 'String1',
};
```



