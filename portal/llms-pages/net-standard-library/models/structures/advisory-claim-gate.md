# Advisory Claim Gate

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkFkdmlzb3J5Q2xhaW1HYXRl

AdvisoryClaimGate.


# Class Name

`AdvisoryClaimGate`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ClaimIndex` | `int` | Required | Claim index.<br><br>**Constraints**: `>= 0`, `<= 19` |
| `ClaimType` | [`ClaimTypeEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/claim-type.md) | Required | Claim type. |
| `ReasonCodes` | [`List<ReasonCodeEnum>`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/reason-code.md) | Required | Reason codes.<br><br>**Constraints**: *Maximum Items*: `10` |
| `Status` | [`StatusEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/status.md) | Required | Status. |
| `TrustedCitationChunkIds` | `List<string>` | Required | Trusted citation chunk ids.<br><br>**Constraints**: *Maximum Items*: `10`, *Pattern*: `^[A-Z0-9-]{1,128}$` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;

AdvisoryClaimGate advisoryClaimGate = new AdvisoryClaimGate
{
    ClaimIndex = 19,
    ClaimType = ClaimTypeEnum.FinancialAction,
    ReasonCodes = new List<ReasonCodeEnum>
    {
        ReasonCodeEnum.CLAIMREFERENCETYPEMISMATCH,
        ReasonCodeEnum.CITATIONTHEMEMISMATCH,
        ReasonCodeEnum.CITATIONREGIONMISMATCH,
    },
    Status = StatusEnum.STRUCTURECOMPATIBLE,
    TrustedCitationChunkIds = new List<string>
    {
        "trusted_citation_chunk_ids6",
        "trusted_citation_chunk_ids7",
        "trusted_citation_chunk_ids8",
    },
};
```



