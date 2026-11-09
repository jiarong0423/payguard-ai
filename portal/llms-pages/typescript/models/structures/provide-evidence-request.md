# Provide Evidence Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlcXVlc3Q

ProvideEvidenceRequest.


# Interface Name

`ProvideEvidenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirmToken` | [`ProvideEvidenceRequestConfirmToken \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/provide-evidence-request-confirm-token.md) | Optional | This is a container for any-of cases. |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `submit` | `boolean \| undefined` | Optional | Submit.<br><br>**Default**: `false` |


# Example

```ts
import { ProvideEvidenceRequest } from 'tradeglot-local-consolelib';

const provideEvidenceRequest: ProvideEvidenceRequest = {
  caseRef: 'case_ref0',
  disputeId: 'dispute_id8',
  confirmToken: 'String7',
  submit: false,
};
```



