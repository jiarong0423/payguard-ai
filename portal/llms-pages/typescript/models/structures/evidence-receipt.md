# Evidence Receipt

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkV2aWRlbmNlUmVjZWlwdA

Evidence receipt.


# Interface Name

`EvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | [`ActionEnum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/action.md) | Optional | Action. |
| `environment` | [`EnvironmentEnum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/environment.md) | Optional | Environment. |
| `evidenceClass` | [`EvidenceClass3Enum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/evidence-class-3.md) | Optional | Evidence class. |
| `externalSend` | [`ExternalSend1Enum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/external-send-1.md) | Optional | External send. |
| `invoiceId` | [`EvidenceReceiptInvoiceId \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/evidence-receipt-invoice-id.md) | Optional | This is a container for any-of cases. |
| `observedAt` | `string \| undefined` | Optional | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypalDebugId` | [`EvidenceReceiptPaypalDebugId \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/evidence-receipt-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `proofKind` | [`ProofKindEnum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/proof-kind.md) | Optional | Proof kind. |
| `schemaVersion` | [`SchemaVersion1Enum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/schema-version-1.md) | Optional | Schema version. |
| `separateGetReadback` | `boolean \| undefined` | Optional | Separate get readback. |
| `status` | [`Status10Enum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-10.md) | Optional | Status. |


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



