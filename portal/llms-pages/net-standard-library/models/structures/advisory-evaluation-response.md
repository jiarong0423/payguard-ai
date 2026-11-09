# Advisory Evaluation Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkFkdmlzb3J5RXZhbHVhdGlvblJlc3BvbnNl

AdvisoryEvaluationResponse.


# Class Name

`AdvisoryEvaluationResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `PIIQuality` | `string` | Required, Constant | PII quality.<br><br>**Value**: `"NOT_EVALUATED"` |
| `AdvisoryOnly` | `bool` | Required | Advisory only. |
| `ClaimCount` | `int` | Required | Claim count.<br><br>**Constraints**: `>= 1`, `<= 20` |
| `ClaimGates` | [`List<AdvisoryClaimGate>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/advisory-claim-gate.md) | Required | Claim gates.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `CorpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CorpusDigests` | [`ReferenceDigests`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `CorpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` |
| `Coverage` | [`PolicyCoverage`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `Limitations` | `List<string>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `ModelGeneration` | `string` | Required, Constant | Model generation.<br><br>**Value**: `"NOT_RUN"` |
| `NaturalLanguageActionAssuranceQuality` | `string` | Required, Constant | Natural language action assurance quality.<br><br>**Value**: `"NOT_EVALUATED"` |
| `OperationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `PromptInjectionQuality` | `string` | Required, Constant | Prompt injection quality.<br><br>**Value**: `"NOT_EVALUATED"` |
| `RequestedContext` | [`PolicyContext`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/policy-context.md) | Required | PolicyContext. |
| `RequiresHumanReview` | `bool` | Required | Requires human review. |
| `SchemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `SemanticEntailment` | `string` | Required, Constant | Semantic entailment.<br><br>**Value**: `"NOT_EVALUATED"` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"offline_structured_gate"` |
| `Status` | [`StatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/status.md) | Required | Status. |
| `Version` | `string` | Required, Constant | Version.<br><br>**Value**: `"payguard.advisory_eval.v1"` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;

AdvisoryEvaluationResponse advisoryEvaluationResponse = new AdvisoryEvaluationResponse
{
    PIIQuality = "NOT_EVALUATED",
    AdvisoryOnly = false,
    ClaimCount = 20,
    ClaimGates = new List<AdvisoryClaimGate>
    {
        new AdvisoryClaimGate
        {
            ClaimIndex = 19,
            ClaimType = ClaimTypeEnum.PolicyReference,
            ReasonCodes = new List<ReasonCodeEnum>
            {
                ReasonCodeEnum.ASSURANCECLAIMFORBIDDEN,
                ReasonCodeEnum.CITATIONUNKNOWN,
                ReasonCodeEnum.CITATIONREGIONMISMATCH,
            },
            Status = StatusEnum.INCOMPLETEEVIDENCE,
            TrustedCitationChunkIds = new List<string>
            {
                "trusted_citation_chunk_ids4",
                "trusted_citation_chunk_ids5",
            },
        },
    },
    CorpusDigest = "corpus_digest4",
    CorpusDigests = new ReferenceDigests
    {
        ChunksSha256 = "chunks_sha2564",
        SourcesSha256 = "sources_sha2562",
    },
    CorpusId = "payguard-us-official-references-v2",
    Coverage = new PolicyCoverage
    {
        Basis = "pinned_authored_summaries_only",
        Complete = false,
        MissingOfficialPolicyThemes = new List<MissingOfficialPolicyThemeEnum>
        {
            MissingOfficialPolicyThemeEnum.SourceCompliance,
        },
        OfficialPolicyChunkCountByTheme = new PolicyThemeCounts
        {
            DisputeMediation = 12,
            SourceCompliance = 29,
            VelocityGuard = 29,
        },
        OfficialPolicySourceIds = new List<string>
        {
            "official_policy_source_ids0",
        },
        RegionalSourceCount = 16,
        SelectedChunkCount = 29,
        SelectedSourceCount = 16,
    },
    CurrentPolicyApplicability = "NOT_ESTABLISHED",
    Limitations = new List<string>
    {
        "limitations3",
        "limitations4",
        "limitations5",
    },
    ModelGeneration = "NOT_RUN",
    NaturalLanguageActionAssuranceQuality = "NOT_EVALUATED",
    OperationalAuthority = "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
    PromptInjectionQuality = "NOT_EVALUATED",
    RequestedContext = new PolicyContext
    {
        AsOf = "as_of8",
        Jurisdiction = "US",
        ObservationMaxAgeDays = 14,
        Theme = ThemeEnum.DisputeMediation,
    },
    RequiresHumanReview = false,
    SchemaVersion = 1,
    SemanticEntailment = "NOT_EVALUATED",
    Source = "offline_structured_gate",
    Status = StatusEnum.INCOMPLETEEVIDENCE,
    Version = "payguard.advisory_eval.v1",
};
```



