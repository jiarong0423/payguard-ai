# Dispute Evidence Row

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVFdmlkZW5jZVJvdw

DisputeEvidenceRow.


# Interface Name

`DisputeEvidenceRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | [`DisputeEvidenceRowAction \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-evidence-row-action.md) | Optional | This is a container for any-of cases. |
| `date` | [`DisputeEvidenceRowDate \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-evidence-row-date.md) | Optional | This is a container for any-of cases. |
| `evidenceType` | `string` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `source` | [`Source3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source-3.md) | Required | Source. |


# Example

```ts
import { DisputeEvidenceRow, Source3Enum } from 'tradeglot-local-consolelib';

const disputeEvidenceRow: DisputeEvidenceRow = {
  evidenceType: 'evidence_type8',
  source: Source3Enum.REQUESTEDFROMSELLER,
  action: 'String7',
  date: 'String3',
};
```



