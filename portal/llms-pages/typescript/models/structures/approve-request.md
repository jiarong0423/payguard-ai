# Approve Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFwcHJvdmVSZXF1ZXN0

ApproveRequest.


# Interface Name

`ApproveRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `draftDigest` | `string` | Required | Draft digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```ts
import { ApproveRequest } from 'tradeglot-local-consolelib';

const approveRequest: ApproveRequest = {
  draftDigest: 'draft_digest6',
};
```



