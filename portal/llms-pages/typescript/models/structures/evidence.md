# Evidence

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkV2aWRlbmNl

Evidence.


# Interface Name

`Evidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrierStatus` | [`EvidenceCarrierStatus \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/evidence-carrier-status.md) | Optional | This is a container for any-of cases. |
| `deliveredAt` | [`EvidenceDeliveredAt \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/evidence-delivered-at.md) | Optional | This is a container for any-of cases. |
| `evidenceSource` | `string` | Required, Constant | Evidence source.<br><br>**Value**: `'synthetic'` |
| `openedAt` | [`EvidenceOpenedAt \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/evidence-opened-at.md) | Optional | This is a container for any-of cases. |
| `orderCreatedAt` | [`EvidenceOrderCreatedAt \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/evidence-order-created-at.md) | Optional | This is a container for any-of cases. |
| `reason` | [`EvidenceReason \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/evidence-reason.md) | Optional | This is a container for any-of cases. |


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



