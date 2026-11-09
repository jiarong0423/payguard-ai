# Evidence Input

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXQ

EvidenceInput.


# Interface Name

`EvidenceInput`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `evidences` | [`EvidenceInputItem[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/evidence-input-item.md) | Required | Evidences.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |


# Example

```ts
import { CarrierNameEnum, EvidenceInput } from 'tradeglot-local-consolelib';

const evidenceInput: EvidenceInput = {
  evidences: [
    {
      evidenceInfo: {
        trackingInfo: [
          {
            carrierName: CarrierNameEnum.DHL,
            trackingNumber: 'tracking_number6',
            carrierNameOther: 'String1',
          }
        ],
      },
      evidenceType: 'evidence_type2',
      notes: 'notes2',
    }
  ],
};
```



