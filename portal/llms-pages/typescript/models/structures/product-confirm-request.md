# Product Confirm Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVxdWVzdA

ProductConfirmRequest.


# Interface Name

`ProductConfirmRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `productId` | [`ProductConfirmRequestProductId`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/product-confirm-request-product-id.md) | Required | This is a container for any-of cases. |


# Example

```ts
import { ProductConfirmRequest } from 'tradeglot-local-consolelib';

const productConfirmRequest: ProductConfirmRequest = {
  description: 'description6',
  evaluationId: 'evaluation_id8',
  productId: 'String1',
};
```



