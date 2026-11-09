# Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkV2aWRlbmNl

Evidence.


# Interface Name

`Evidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrierStatus` | [`EvidenceCarrierStatus \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/evidence-carrier-status.md) | Optional | This is a container for any-of cases. |
| `deliveredAt` | [`EvidenceDeliveredAt \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/evidence-delivered-at.md) | Optional | This is a container for any-of cases. |
| `evidenceSource` | `string` | Required, Constant | Evidence source.<br><br>**Value**: `'synthetic'` |
| `openedAt` | [`EvidenceOpenedAt \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/evidence-opened-at.md) | Optional | This is a container for any-of cases. |
| `orderCreatedAt` | [`EvidenceOrderCreatedAt \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/evidence-order-created-at.md) | Optional | This is a container for any-of cases. |
| `reason` | [`EvidenceReason \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/evidence-reason.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import { Evidence } from 'tradeglot-local-consolelib';

const evidence: Evidence = {
  evidenceSource: 'synthetic',
  carrierStatus: 'String5',
  deliveredAt: 'String1',
  openedAt: 'String1',
  orderCreatedAt: 'String3',
  reason: 'String3',
};
```



