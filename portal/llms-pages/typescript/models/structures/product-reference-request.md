# Product Reference Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXF1ZXN0

ProductReferenceRequest.


# Interface Name

`ProductReferenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```ts
import { ProductReferenceRequest } from 'tradeglot-local-consolelib';

const productReferenceRequest: ProductReferenceRequest = {
  description: 'description8',
  evaluationId: 'evaluation_id2',
};
```



