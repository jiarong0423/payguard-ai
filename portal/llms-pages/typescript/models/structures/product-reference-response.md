# Product Reference Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXNwb25zZQ

Up to three Channel3 products for the seller to pick from; advisory, never changes the AUP decision.


# Interface Name

`ProductReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` |
| `cards` | [`ProductCard[]`](http://localhost:3000/llms-pages/typescript/models/structures/product-card.md) | Required | Cards.<br><br>**Constraints**: *Maximum Items*: `3` |
| `reason` | [`ProductReferenceResponseReason`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/product-reference-response-reason.md) | Required | This is a container for any-of cases. |
| `recordedAt` | [`ProductReferenceResponseRecordedAt`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/product-reference-response-recorded-at.md) | Required | This is a container for any-of cases. |
| `source` | [`ProductReferenceResponseSource`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/product-reference-response-source.md) | Required | This is a container for any-of cases. |
| `status` | [`Status12Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-12.md) | Required | Status. |


# Example

```ts
import {
  ProductReferenceResponse,
  Reason7Enum,
  Source11Enum,
  Status12Enum,
} from 'tradeglot-local-consolelib';

const productReferenceResponse: ProductReferenceResponse = {
  affectsDecision: 'False',
  cards: [
    {
      brand: 'String3',
      category: 'String7',
      imageUrl: 'String5',
      keyFeatures: [
        'key_features4',
        'key_features5',
        'key_features6'
      ],
      materials: [
        'materials9',
        'materials0'
      ],
      productId: 'product_id4',
      title: 'title4',
    }
  ],
  reason: Reason7Enum.NothingToSend,
  recordedAt: 'String9',
  source: Source11Enum.Channel3Live,
  status: Status12Enum.NOTFOUND,
};
```



