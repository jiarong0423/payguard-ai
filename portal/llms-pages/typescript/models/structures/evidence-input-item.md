# Evidence Input Item

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXRJdGVt

EvidenceInputItem.


# Interface Name

`EvidenceInputItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `evidenceInfo` | [`EvidenceInfo`](http://localhost:3000/llms-pages/typescript/models/structures/evidence-info.md) | Required | EvidenceInfo. |
| `evidenceType` | `string` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `notes` | `string` | Required | Notes.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```ts
import {
  CarrierNameEnum,
  EvidenceInputItem,
} from 'tradeglot-local-consolelib';

const evidenceInputItem: EvidenceInputItem = {
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
};
```



