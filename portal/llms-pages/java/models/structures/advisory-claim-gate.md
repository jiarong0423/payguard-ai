# Advisory Claim Gate

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkFkdmlzb3J5Q2xhaW1HYXRl

AdvisoryClaimGate.


# Class Name

`AdvisoryClaimGate`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `ClaimIndex` | `int` | Required | Claim index.<br><br>**Constraints**: `>= 0`, `<= 19` | int getClaimIndex() | setClaimIndex(int claimIndex) |
| `ClaimType` | [`ClaimTypeEnum`](http://localhost:3000/llms-pages/java/models/enumerations/claim-type.md) | Required | Claim type. | ClaimTypeEnum getClaimType() | setClaimType(ClaimTypeEnum claimType) |
| `ReasonCodes` | [`List<ReasonCodeEnum>`](http://localhost:3000/llms-pages/java/models/enumerations/reason-code.md) | Required | Reason codes.<br><br>**Constraints**: *Maximum Items*: `10` | List<ReasonCodeEnum> getReasonCodes() | setReasonCodes(List<ReasonCodeEnum> reasonCodes) |
| `Status` | [`StatusEnum`](http://localhost:3000/llms-pages/java/models/enumerations/status.md) | Required | Status. | StatusEnum getStatus() | setStatus(StatusEnum status) |
| `TrustedCitationChunkIds` | `List<String>` | Required | Trusted citation chunk ids.<br><br>**Constraints**: *Maximum Items*: `10`, *Pattern*: `^[A-Z0-9-]{1,128}$` | List<String> getTrustedCitationChunkIds() | setTrustedCitationChunkIds(List<String> trustedCitationChunkIds) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.AdvisoryClaimGate;
import m18000.m0.m0.m127.models.ClaimTypeEnum;
import m18000.m0.m0.m127.models.ReasonCodeEnum;
import m18000.m0.m0.m127.models.StatusEnum;

AdvisoryClaimGate advisoryClaimGate = new AdvisoryClaimGate.Builder(
    19,
    ClaimTypeEnum.FINANCIAL_ACTION,
    Arrays.asList(
        ReasonCodeEnum.CLAIM_REFERENCE_TYPE_MISMATCH,
        ReasonCodeEnum.CITATION_THEME_MISMATCH,
        ReasonCodeEnum.CITATION_REGION_MISMATCH
    ),
    StatusEnum.STRUCTURE_COMPATIBLE,
    Arrays.asList(
        "trusted_citation_chunk_ids6",
        "trusted_citation_chunk_ids7",
        "trusted_citation_chunk_ids8"
    )
)
.build();
```



