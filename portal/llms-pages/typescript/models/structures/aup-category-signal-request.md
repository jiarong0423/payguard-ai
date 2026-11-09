# Aup Category Signal Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVxdWVzdA

AupCategorySignalRequest.


# Interface Name

`AupCategorySignalRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```ts
import { AupCategorySignalRequest } from 'tradeglot-local-consolelib';

const aupCategorySignalRequest: AupCategorySignalRequest = {
  description: 'description0',
  evaluationId: 'evaluation_id4',
};
```



