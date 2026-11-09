# Reference Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlc3BvbnNl

ReferenceResponse.


# Class Name

`ReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `bool` | Required | Advisory only. |
| `CorpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CorpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/net-standard-library/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `CorpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` |
| `FiltersApplied` | [`ReferenceFilters`](http://localhost:3000/llms-pages/net-standard-library/models/structures/reference-filters.md) | Required | ReferenceFilters. |
| `Limitations` | `List<string>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `OperationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `Results` | [`List<ReferenceCitation>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/reference-citation.md) | Required | Results.<br><br>**Constraints**: *Maximum Items*: `10` |
| `SchemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"public_reference"` |
| `Status` | [`Status13Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/status-13.md) | Required | Status. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

ReferenceResponse referenceResponse = new ReferenceResponse
{
    AdvisoryOnly = false,
    CorpusDigest = "corpus_digest2",
    CorpusDigests = new ReferenceDigests
    {
        ChunksSha256 = "chunks_sha2564",
        SourcesSha256 = "sources_sha2562",
    },
    CorpusId = "payguard-us-official-references-v2",
    FiltersApplied = new ReferenceFilters
    {
        AgeBasis = "source_updated_date_utc_calendar",
        AsOf = ReferenceFiltersAsOf.FromString("String1"),
        CaseStage = CaseStage2Enum.ProceduralOrder,
        Jurisdiction = "US",
        Limit = 10,
        MaterialTypes = new List<MaterialType4Enum>
        {
            MaterialType4Enum.OfficialPolicy,
            MaterialType4Enum.PublicCourtOrderCopy,
        },
        MaxSourceAgeDays = ReferenceFiltersMaxSourceAgeDays.FromNumber(28),
        RequireKnownSourceDate = false,
        Theme = ThemeEnum.DisputeMediation,
    },
    Limitations = new List<string>
    {
        "limitations5",
        "limitations6",
    },
    OperationalAuthority = "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
    Results = new List<ReferenceCitation>
    {
        new ReferenceCitation
        {
            CaseOutcome = ReferenceCitationCaseOutcome.FromCaseOutcome(CaseOutcomeEnum.SETTLEMENTAPPROVALNOTFINALMERITS),
            CaseStage = CaseStageEnum.ProceduralOrder,
            ChunkId = "chunk_id2",
            DecisionAcceptanceDeadline = ReferenceCitationDecisionAcceptanceDeadline.FromString("String5"),
            DecisionDate = ReferenceCitationDecisionDate.FromString("String9"),
            DecisionDateStatus = DecisionDateStatusEnum.NOTAPPLICABLE,
            EffectiveDate = ReferenceCitationEffectiveDate.FromString("String5"),
            EffectiveDateStatus = EffectiveDateStatusEnum.DOCUMENTSTATED,
            Jurisdiction = "US",
            JurisdictionLabel = "jurisdiction_label4",
            Locator = "locator8",
            MaterialType = MaterialType1Enum.OfficialApiReference,
            RelevanceScore = 128,
            RetrievedAt = "retrieved_at0",
            SourceId = "source_id0",
            SourceTitle = "source_title8",
            SourceUpdatedDate = ReferenceCitationSourceUpdatedDate.FromString("String9"),
            SourceUpdatedDateStatus = SourceUpdatedDateStatusEnum.DOCUMENTSTATED,
            Text = "text4",
            TextSha256 = "text_sha2566",
            Title = "title8",
            Url = "url0",
        },
    },
    SchemaVersion = 1,
    Source = "public_reference",
    Status = Status13Enum.ReferencesFound,
};
```



