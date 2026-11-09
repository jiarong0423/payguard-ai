# Add Tracking Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVxdWVzdA

AddTrackingRequest.


# Interface Name

`AddTrackingRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirmToken` | [`AddTrackingRequestConfirmToken \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/add-tracking-request-confirm-token.md) | Optional | This is a container for any-of cases. |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `submit` | `boolean \| undefined` | Optional | Submit.<br><br>**Default**: `false` |


# Example

```ts
import { AddTrackingRequest } from 'tradeglot-local-consolelib';

const addTrackingRequest: AddTrackingRequest = {
  caseRef: 'case_ref4',
  disputeId: 'dispute_id2',
  confirmToken: 'String1',
  submit: false,
};
```



