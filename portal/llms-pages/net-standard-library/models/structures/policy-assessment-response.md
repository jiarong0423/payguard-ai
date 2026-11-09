# Policy Assessment Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlBvbGljeUFzc2Vzc21lbnRSZXNwb25zZQ

PolicyAssessmentResponse.


# Class Name

`PolicyAssessmentResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `bool` | Required | Advisory only. |
| `Chunks` | [`List<PolicyChunk>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/policy-chunk.md) | Required | Chunks.<br><br>**Constraints**: *Maximum Items*: `29` |
| `CorpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CorpusDigests` | [`ReferenceDigests`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `CorpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` |
| `Coverage` | [`PolicyCoverage`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `FiltersApplied` | [`PolicyContext`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/policy-context.md) | Required | PolicyContext. |
| `Limitations` | `List<string>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `OperationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `ReasonCodes` | [`List<ReasonCode1Enum>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `RequiresHumanReview` | `bool` | Required | Requires human review. |
| `SchemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"public_reference"` |
| `Sources` | [`List<PolicySource>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/policy-source.md) | Required | Sources.<br><br>**Constraints**: *Maximum Items*: `16` |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"INCOMPLETE_POLICY_EVIDENCE"` |
| `Version` | `string` | Required, Constant | Version.<br><br>**Value**: `"payguard.applicability.v1"` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

PolicyAssessmentResponse policyAssessmentResponse = new PolicyAssessmentResponse
{
    AdvisoryOnly = false,
    Chunks = new List<PolicyChunk>
    {
        new PolicyChunk
        {
            CaseOutcome = PolicyChunkCaseOutcome.FromCaseOutcome(CaseOutcomeEnum.SETTLEMENTAPPROVALNOTFINALMERITS),
            CaseStage = CaseStageEnum.ProceduralOrder,
            ChunkId = "chunk_id6",
            Jurisdiction = "US",
            MaterialType = MaterialType1Enum.OfficialPolicy,
            SourceId = "source_id6",
            TextSha256 = "text_sha2560",
            Theme = ThemeEnum.VelocityGuard,
        },
    },
    CorpusDigest = "corpus_digest2",
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
    FiltersApplied = new PolicyContext
    {
        AsOf = "as_of0",
        Jurisdiction = "US",
        ObservationMaxAgeDays = 28,
        Theme = ThemeEnum.DisputeMediation,
    },
    Limitations = new List<string>
    {
        "limitations5",
        "limitations4",
        "limitations3",
    },
    OperationalAuthority = "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
    ReasonCodes = new List<ReasonCode1Enum>
    {
        ReasonCode1Enum.CURRENTPOLICYAPPLICABILITYNOTESTABLISHED,
        ReasonCode1Enum.FUTUREOBSERVATION,
    },
    RequiresHumanReview = false,
    SchemaVersion = 1,
    Source = "public_reference",
    Sources = new List<PolicySource>
    {
        new PolicySource
        {
            CitationChunkIds = new List<string>
            {
                "citation_chunk_ids2",
                "citation_chunk_ids3",
            },
            ContentClass = "public_reference_summary",
            CurrentPolicyApplicability = "NOT_ESTABLISHED",
            DecisionAcceptanceDeadline = PolicySourceDecisionAcceptanceDeadline.FromString("String5"),
            DecisionDate = PolicySourceDecisionDate.FromString("String9"),
            DecisionDateStatus = DecisionDateStatusEnum.DOCUMENTSTATED,
            EffectiveDate = PolicySourceEffectiveDate.FromString("String7"),
            EffectiveDateStatus = EffectiveDateStatusEnum.DOCUMENTSTATED,
            Jurisdiction = "jurisdiction0",
            JurisdictionNormalized = "US",
            MaterialType = MaterialType1Enum.PublicCourtOrderCopy,
            ObservationAgeBasis = "saved_retrieved_at_exact_elapsed_time",
            ObservationStatus = ObservationStatusEnum.FUTUREOBSERVATION,
            ReasonCodes = new List<ReasonCode1Enum>
            {
                ReasonCode1Enum.CURRENTPOLICYAPPLICABILITYNOTESTABLISHED,
                ReasonCode1Enum.FUTUREOBSERVATION,
            },
            Representation = "authored_paraphrase_not_full_source",
            RetrievedAt = "retrieved_at0",
            SourceId = "source_id0",
            SourceUpdatedDate = PolicySourceSourceUpdatedDate.FromString("String9"),
            SourceUpdatedDateStatus = SourceUpdatedDateStatusEnum.DOCUMENTSTATED,
            Title = "title2",
            Url = "url0",
        },
    },
    Status = "INCOMPLETE_POLICY_EVIDENCE",
    Version = "payguard.applicability.v1",
};
```



