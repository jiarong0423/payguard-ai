# Advisory Evaluation Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFkdmlzb3J5RXZhbHVhdGlvblJlc3BvbnNl

AdvisoryEvaluationResponse.


# Interface Name

`AdvisoryEvaluationResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `pIIQuality` | `string` | Required, Constant | PII quality.<br><br>**Value**: `'NOT_EVALUATED'` |
| `advisoryOnly` | `boolean` | Required | Advisory only. |
| `claimCount` | `number` | Required | Claim count.<br><br>**Constraints**: `>= 1`, `<= 20` |
| `claimGates` | [`AdvisoryClaimGate[]`](http://localhost:3000/llms-pages/typescript/models/structures/advisory-claim-gate.md) | Required | Claim gates.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `corpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/typescript/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `corpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `'payguard-us-official-references-v2'` |
| `coverage` | [`PolicyCoverage`](http://localhost:3000/llms-pages/typescript/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `modelGeneration` | `string` | Required, Constant | Model generation.<br><br>**Value**: `'NOT_RUN'` |
| `naturalLanguageActionAssuranceQuality` | `string` | Required, Constant | Natural language action assurance quality.<br><br>**Value**: `'NOT_EVALUATED'` |
| `operationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` |
| `promptInjectionQuality` | `string` | Required, Constant | Prompt injection quality.<br><br>**Value**: `'NOT_EVALUATED'` |
| `requestedContext` | [`PolicyContext`](http://localhost:3000/llms-pages/typescript/models/structures/policy-context.md) | Required | PolicyContext. |
| `requiresHumanReview` | `boolean` | Required | Requires human review. |
| `schemaVersion` | `number` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `semanticEntailment` | `string` | Required, Constant | Semantic entailment.<br><br>**Value**: `'NOT_EVALUATED'` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'offline_structured_gate'` |
| `status` | [`StatusEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status.md) | Required | Status. |
| `version` | `string` | Required, Constant | Version.<br><br>**Value**: `'payguard.advisory_eval.v1'` |


# Example

```ts
import {
  AdvisoryEvaluationResponse,
  ClaimTypeEnum,
  MissingOfficialPolicyThemeEnum,
  ReasonCodeEnum,
  StatusEnum,
  ThemeEnum,
} from 'tradeglot-local-consolelib';

const advisoryEvaluationResponse: AdvisoryEvaluationResponse = {
  pIIQuality: 'NOT_EVALUATED',
  advisoryOnly: false,
  claimCount: 20,
  claimGates: [
    {
      claimIndex: 19,
      claimType: ClaimTypeEnum.PolicyReference,
      reasonCodes: [
        ReasonCodeEnum.ASSURANCECLAIMFORBIDDEN,
        ReasonCodeEnum.CITATIONUNKNOWN,
        ReasonCodeEnum.CITATIONREGIONMISMATCH
      ],
      status: StatusEnum.INCOMPLETEEVIDENCE,
      trustedCitationChunkIds: [
        'trusted_citation_chunk_ids4',
        'trusted_citation_chunk_ids5'
      ],
    }
  ],
  corpusDigest: 'corpus_digest4',
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
  limitations: [
    'limitations3',
    'limitations4',
    'limitations5'
  ],
  modelGeneration: 'NOT_RUN',
  naturalLanguageActionAssuranceQuality: 'NOT_EVALUATED',
  operationalAuthority: 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  promptInjectionQuality: 'NOT_EVALUATED',
  requestedContext: {
    asOf: 'as_of8',
    jurisdiction: 'US',
    observationMaxAgeDays: 14,
    theme: ThemeEnum.DisputeMediation,
  },
  requiresHumanReview: false,
  schemaVersion: 1,
  semanticEntailment: 'NOT_EVALUATED',
  source: 'offline_structured_gate',
  status: StatusEnum.INCOMPLETEEVIDENCE,
  version: 'payguard.advisory_eval.v1',
};
```



