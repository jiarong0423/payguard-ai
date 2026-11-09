# Advisory Claim Gate

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkFkdmlzb3J5Q2xhaW1HYXRl

AdvisoryClaimGate.


# Class Name

`AdvisoryClaimGate`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `claimIndex` | `int` | Required | Claim index.<br><br>**Constraints**: `>= 0`, `<= 19` | getClaimIndex(): int | setClaimIndex(int claimIndex): void |
| `claimType` | [`string(ClaimTypeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/claim-type.md) | Required | Claim type. | getClaimType(): string | setClaimType(string claimType): void |
| `reasonCodes` | [`string(ReasonCodeEnum)[]`](http://localhost:3000/llms-pages/php/models/enumerations/reason-code.md) | Required | Reason codes.<br><br>**Constraints**: *Maximum Items*: `10` | getReasonCodes(): array | setReasonCodes(array reasonCodes): void |
| `status` | [`string(StatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/status.md) | Required | Status. | getStatus(): string | setStatus(string status): void |
| `trustedCitationChunkIds` | `string[]` | Required | Trusted citation chunk ids.<br><br>**Constraints**: *Maximum Items*: `10`, *Pattern*: `^[A-Z0-9-]{1,128}$` | getTrustedCitationChunkIds(): array | setTrustedCitationChunkIds(array trustedCitationChunkIds): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AdvisoryClaimGateBuilder;
use TradeGlotLocalConsoleLib\Models\ClaimTypeEnum;
use TradeGlotLocalConsoleLib\Models\ReasonCodeEnum;
use TradeGlotLocalConsoleLib\Models\StatusEnum;

$advisoryClaimGate = AdvisoryClaimGateBuilder::init(
    19,
    ClaimTypeEnum::FINANCIAL_ACTION,
    [
        ReasonCodeEnum::CLAIM_REFERENCE_TYPE_MISMATCH,
        ReasonCodeEnum::CITATION_THEME_MISMATCH,
        ReasonCodeEnum::CITATION_REGION_MISMATCH
    ],
    StatusEnum::STRUCTURE_COMPATIBLE,
    [
        'trusted_citation_chunk_ids6',
        'trusted_citation_chunk_ids7',
        'trusted_citation_chunk_ids8'
    ]
)->build();
```



