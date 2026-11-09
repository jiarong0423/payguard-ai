# Product Confirm Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2U

The seller's own choice: one of the cards they were shown, or none of them.


# Interface Name

`ProductConfirmResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` |
| `card` | [`ProductConfirmResponseCard`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/product-confirm-response-card.md) | Required | This is a container for any-of cases. |
| `cardDigest` | [`ProductConfirmResponseCardDigest`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/product-confirm-response-card-digest.md) | Required | This is a container for any-of cases. |
| `choice` | [`Choice2Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/choice-2.md) | Required | Choice. |
| `confirmedBy` | `string` | Required, Constant | Confirmed by.<br><br>**Value**: `'seller'` |
| `descriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `recordedAt` | [`ProductConfirmResponseRecordedAt`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/product-confirm-response-recorded-at.md) | Required | This is a container for any-of cases. |
| `source` | [`Source10Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/source-10.md) | Required | Source. |


# Example

```ts
import {
  Choice2Enum,
  ProductConfirmResponse,
  Source10Enum,
} from 'tradeglot-local-consolelib';

const productConfirmResponse: ProductConfirmResponse = {
  affectsDecision: 'False',
  card: {
    brand: 'String9',
    category: 'String3',
    imageUrl: 'String1',
    keyFeatures: [
      'key_features0',
      'key_features1',
      'key_features2'
    ],
    materials: [
      'materials5',
      'materials6'
    ],
    productId: 'product_id0',
    title: 'title0',
  },
  cardDigest: 'String1',
  choice: Choice2Enum.CONFIRMED,
  confirmedBy: 'seller',
  descriptionDigest: 'description_digest2',
  evaluationId: 'evaluation_id8',
  recordedAt: 'String1',
  source: Source10Enum.Channel3Live,
};
```



