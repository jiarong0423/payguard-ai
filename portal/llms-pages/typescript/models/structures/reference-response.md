# Reference Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlc3BvbnNl

ReferenceResponse.


# Interface Name

`ReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisoryOnly` | `boolean` | Required | Advisory only. |
| `corpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/typescript/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `corpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `'payguard-us-official-references-v2'` |
| `filtersApplied` | [`ReferenceFilters`](http://localhost:3000/llms-pages/typescript/models/structures/reference-filters.md) | Required | ReferenceFilters. |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `operationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` |
| `results` | [`ReferenceCitation[]`](http://localhost:3000/llms-pages/typescript/models/structures/reference-citation.md) | Required | Results.<br><br>**Constraints**: *Maximum Items*: `10` |
| `schemaVersion` | `number` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'public_reference'` |
| `status` | [`Status13Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-13.md) | Required | Status. |


# Example

```ts
import {
  CaseOutcomeEnum,
  CaseStage2Enum,
  CaseStageEnum,
  DecisionDateStatusEnum,
  EffectiveDateStatusEnum,
  MaterialType1Enum,
  MaterialType4Enum,
  ReferenceResponse,
  SourceUpdatedDateStatusEnum,
  Status13Enum,
  ThemeEnum,
} from 'tradeglot-local-consolelib';

const referenceResponse: ReferenceResponse = {
  advisoryOnly: false,
  corpusDigest: 'corpus_digest2',
  corpusDigests: {
    chunksSha256: 'chunks_sha2564',
    sourcesSha256: 'sources_sha2562',
  },
  corpusId: 'payguard-us-official-references-v2',
  filtersApplied: {
    ageBasis: 'source_updated_date_utc_calendar',
    asOf: 'String1',
    caseStage: CaseStage2Enum.ProceduralOrder,
    jurisdiction: 'US',
    limit: 10,
    materialTypes: [
      MaterialType4Enum.OfficialPolicy,
      MaterialType4Enum.PublicCourtOrderCopy
    ],
    maxSourceAgeDays: 28,
    requireKnownSourceDate: false,
    theme: ThemeEnum.DisputeMediation,
  },
  limitations: [
    'limitations5',
    'limitations6'
  ],
  operationalAuthority: 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  results: [
    {
      caseOutcome: CaseOutcomeEnum.SETTLEMENTAPPROVALNOTFINALMERITS,
      caseStage: CaseStageEnum.ProceduralOrder,
      chunkId: 'chunk_id2',
      decisionAcceptanceDeadline: 'String5',
      decisionDate: 'String9',
      decisionDateStatus: DecisionDateStatusEnum.NOTAPPLICABLE,
      effectiveDate: 'String5',
      effectiveDateStatus: EffectiveDateStatusEnum.DOCUMENTSTATED,
      jurisdiction: 'US',
      jurisdictionLabel: 'jurisdiction_label4',
      locator: 'locator8',
      materialType: MaterialType1Enum.OfficialApiReference,
      relevanceScore: 128,
      retrievedAt: 'retrieved_at0',
      sourceId: 'source_id0',
      sourceTitle: 'source_title8',
      sourceUpdatedDate: 'String9',
      sourceUpdatedDateStatus: SourceUpdatedDateStatusEnum.DOCUMENTSTATED,
      text: 'text4',
      textSha256: 'text_sha2566',
      title: 'title8',
      url: 'url0',
    }
  ],
  schemaVersion: 1,
  source: 'public_reference',
  status: Status13Enum.ReferencesFound,
};
```



