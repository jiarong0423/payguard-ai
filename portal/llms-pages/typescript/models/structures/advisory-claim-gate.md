# Advisory Claim Gate

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFkdmlzb3J5Q2xhaW1HYXRl

AdvisoryClaimGate.


# Interface Name

`AdvisoryClaimGate`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `claimIndex` | `number` | Required | Claim index.<br><br>**Constraints**: `>= 0`, `<= 19` |
| `claimType` | [`ClaimTypeEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/claim-type.md) | Required | Claim type. |
| `reasonCodes` | [`ReasonCodeEnum[]`](http://localhost:3000/llms-pages/typescript/models/enumerations/reason-code.md) | Required | Reason codes.<br><br>**Constraints**: *Maximum Items*: `10` |
| `status` | [`StatusEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status.md) | Required | Status. |
| `trustedCitationChunkIds` | `string[]` | Required | Trusted citation chunk ids.<br><br>**Constraints**: *Maximum Items*: `10`, *Pattern*: `^[A-Z0-9-]{1,128}$` |


# Example

```ts
import {
  AdvisoryClaimGate,
  ClaimTypeEnum,
  ReasonCodeEnum,
  StatusEnum,
} from 'tradeglot-local-consolelib';

const advisoryClaimGate: AdvisoryClaimGate = {
  claimIndex: 19,
  claimType: ClaimTypeEnum.FinancialAction,
  reasonCodes: [
    ReasonCodeEnum.CLAIMREFERENCETYPEMISMATCH,
    ReasonCodeEnum.CITATIONTHEMEMISMATCH,
    ReasonCodeEnum.CITATIONREGIONMISMATCH
  ],
  status: StatusEnum.STRUCTURECOMPATIBLE,
  trustedCitationChunkIds: [
    'trusted_citation_chunk_ids6',
    'trusted_citation_chunk_ids7',
    'trusted_citation_chunk_ids8'
  ],
};
```



