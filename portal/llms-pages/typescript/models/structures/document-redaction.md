# Document Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkRvY3VtZW50UmVkYWN0aW9u

DocumentRedaction.


# Interface Name

`DocumentRedaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `counts` | `Record<string, number>` | Required | Counts.<br><br>**Constraints**: `>= 1`, `<= 128` |
| `exportProfile` | `string` | Required, Constant | Export profile.<br><br>**Value**: `'INTERNAL_REVIEW_ONLY_V1'` |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `limitedDetection` | `string` | Required, Constant | Limited detection.<br><br>**Value**: `'True'` |
| `manualReviewRequired` | `string` | Required, Constant | Manual review required.<br><br>**Value**: `'True'` |
| `method` | `string` | Required, Constant | Method.<br><br>**Value**: `'HMAC-SHA256 document pseudonymization v1'` |
| `redactedText` | `string` | Required | Redacted text.<br><br>**Constraints**: *Maximum Length*: `32768` |
| `replacementCount` | `number` | Required | Replacement count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `reversibility` | `string` | Required, Constant | Reversibility.<br><br>**Value**: `'False'` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `types` | [`TypeEnum[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/type.md) | Required | Types.<br><br>**Constraints**: *Maximum Items*: `7` |


# Example

```ts
import { DocumentRedaction, TypeEnum } from 'tradeglot-local-consolelib';

const documentRedaction: DocumentRedaction = {
  counts: {
    'key0': 128,
    'key1': 1,
    'key2': 1
  },
  exportProfile: 'INTERNAL_REVIEW_ONLY_V1',
  limitations: [
    'limitations3'
  ],
  limitedDetection: 'True',
  manualReviewRequired: 'True',
  method: 'HMAC-SHA256 document pseudonymization v1',
  redactedText: 'redacted_text2',
  replacementCount: 128,
  reversibility: 'False',
  source: 'synthetic',
  types: [
    TypeEnum.IdLike,
    TypeEnum.Name,
    TypeEnum.Address
  ],
};
```



