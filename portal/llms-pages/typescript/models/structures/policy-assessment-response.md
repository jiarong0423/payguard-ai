# Policy Assessment Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlBvbGljeUFzc2Vzc21lbnRSZXNwb25zZQ

PolicyAssessmentResponse.


# Interface Name

`PolicyAssessmentResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisoryOnly` | `boolean` | Required | Advisory only. |
| `chunks` | [`PolicyChunk[]`](http://localhost:3000/llms-pages/typescript/models/structures/policy-chunk.md) | Required | Chunks.<br><br>**Constraints**: *Maximum Items*: `29` |
| `corpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/typescript/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `corpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `'payguard-us-official-references-v2'` |
| `coverage` | [`PolicyCoverage`](http://localhost:3000/llms-pages/typescript/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `filtersApplied` | [`PolicyContext`](http://localhost:3000/llms-pages/typescript/models/structures/policy-context.md) | Required | PolicyContext. |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `operationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` |
| `reasonCodes` | [`ReasonCode1Enum[]`](http://localhost:3000/llms-pages/typescript/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `requiresHumanReview` | `boolean` | Required | Requires human review. |
| `schemaVersion` | `number` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'public_reference'` |
| `sources` | [`PolicySource[]`](http://localhost:3000/llms-pages/typescript/models/structures/policy-source.md) | Required | Sources.<br><br>**Constraints**: *Maximum Items*: `16` |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'INCOMPLETE_POLICY_EVIDENCE'` |
| `version` | `string` | Required, Constant | Version.<br><br>**Value**: `'payguard.applicability.v1'` |


# Example

```ts
import {
  CaseOutcomeEnum,
  CaseStageEnum,
  DecisionDateStatusEnum,
  EffectiveDateStatusEnum,
  MaterialType1Enum,
  MissingOfficialPolicyThemeEnum,
  ObservationStatusEnum,
  PolicyAssessmentResponse,
  ReasonCode1Enum,
  SourceUpdatedDateStatusEnum,
  ThemeEnum,
} from 'tradeglot-local-consolelib';

const policyAssessmentResponse: PolicyAssessmentResponse = {
  advisoryOnly: false,
  chunks: [
    {
      caseOutcome: CaseOutcomeEnum.SETTLEMENTAPPROVALNOTFINALMERITS,
      caseStage: CaseStageEnum.ProceduralOrder,
      chunkId: 'chunk_id6',
      jurisdiction: 'US',
      materialType: MaterialType1Enum.OfficialPolicy,
      sourceId: 'source_id6',
      textSha256: 'text_sha2560',
      theme: ThemeEnum.VelocityGuard,
    }
  ],
  corpusDigest: 'corpus_digest2',
  corpusDigests: {
    chunksSha256: 'chunks_sha2564',
    sourcesSha256: 'sources_sha2562',
  },
  corpusId: 'payguard-us-official-references-v2',
  coverage: {
    basis: 'pinned_authored_summaries_only',
    complete: false,
    missingOfficialPolicyThemes: [
      MissingOfficialPolicyThemeEnum.SourceCompliance
    ],
    officialPolicyChunkCountByTheme: {
      disputeMediation: 12,
      sourceCompliance: 29,
      velocityGuard: 29,
    },
    officialPolicySourceIds: [
      'official_policy_source_ids0'
    ],
    regionalSourceCount: 16,
    selectedChunkCount: 29,
    selectedSourceCount: 16,
  },
  currentPolicyApplicability: 'NOT_ESTABLISHED',
  filtersApplied: {
    asOf: 'as_of0',
    jurisdiction: 'US',
    observationMaxAgeDays: 28,
    theme: ThemeEnum.DisputeMediation,
  },
  limitations: [
    'limitations5',
    'limitations4',
    'limitations3'
  ],
  operationalAuthority: 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  reasonCodes: [
    ReasonCode1Enum.CURRENTPOLICYAPPLICABILITYNOTESTABLISHED,
    ReasonCode1Enum.FUTUREOBSERVATION
  ],
  requiresHumanReview: false,
  schemaVersion: 1,
  source: 'public_reference',
  sources: [
    {
      citationChunkIds: [
        'citation_chunk_ids2',
        'citation_chunk_ids3'
      ],
      contentClass: 'public_reference_summary',
      currentPolicyApplicability: 'NOT_ESTABLISHED',
      decisionAcceptanceDeadline: 'String5',
      decisionDate: 'String9',
      decisionDateStatus: DecisionDateStatusEnum.DOCUMENTSTATED,
      effectiveDate: 'String7',
      effectiveDateStatus: EffectiveDateStatusEnum.DOCUMENTSTATED,
      jurisdiction: 'jurisdiction0',
      jurisdictionNormalized: 'US',
      materialType: MaterialType1Enum.PublicCourtOrderCopy,
      observationAgeBasis: 'saved_retrieved_at_exact_elapsed_time',
      observationStatus: ObservationStatusEnum.FUTUREOBSERVATION,
      reasonCodes: [
        ReasonCode1Enum.CURRENTPOLICYAPPLICABILITYNOTESTABLISHED,
        ReasonCode1Enum.FUTUREOBSERVATION
      ],
      representation: 'authored_paraphrase_not_full_source',
      retrievedAt: 'retrieved_at0',
      sourceId: 'source_id0',
      sourceUpdatedDate: 'String9',
      sourceUpdatedDateStatus: SourceUpdatedDateStatusEnum.DOCUMENTSTATED,
      title: 'title2',
      url: 'url0',
    }
  ],
  status: 'INCOMPLETE_POLICY_EVIDENCE',
  version: 'payguard.applicability.v1',
};
```



