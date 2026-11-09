# Scenario Match

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlNjZW5hcmlvTWF0Y2g

ScenarioMatch.


# Interface Name

`ScenarioMatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `engineExecution` | `string` | Required, Constant | Engine execution.<br><br>**Value**: `'NOT_RUN'` |
| `evaluationScope` | `string` | Required, Constant | Evaluation scope.<br><br>**Value**: `'AUTHORED_SYNTHETIC_DEMO_ONLY'` |
| `intakeStatus` | [`IntakeStatusEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/intake-status.md) | Required | Intake status. |
| `operationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` |
| `provenance` | `string` | Required, Constant | Provenance.<br><br>**Value**: `'AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES'` |
| `realCaseEvidence` | `string` | Required, Constant | Real case evidence.<br><br>**Value**: `'NOT_PROVIDED'` |
| `requiredHumanReview` | `string` | Required, Constant | Required human review.<br><br>**Value**: `'True'` |
| `scenario` | [`DisputeScenario`](http://localhost:3000/llms-pages/typescript/models/structures/dispute-scenario.md) | Required | DisputeScenario. |
| `schemaVersion` | `number` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'local_synthetic_scenario_matcher'` |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'synthetic_scenarios_found'` |


# Example

```ts
import {
  IntakeStatusEnum,
  MaterialTypeEnum,
  ScenarioMatch,
} from 'tradeglot-local-consolelib';

const scenarioMatch: ScenarioMatch = {
  currentPolicyApplicability: 'NOT_ESTABLISHED',
  engineExecution: 'NOT_RUN',
  evaluationScope: 'AUTHORED_SYNTHETIC_DEMO_ONLY',
  intakeStatus: IntakeStatusEnum.ReadyForLocalRules,
  operationalAuthority: 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  provenance: 'AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES',
  realCaseEvidence: 'NOT_PROVIDED',
  requiredHumanReview: 'True',
  scenario: {
    citations: [
      {
        chunkId: 'chunk_id0',
        jurisdiction: 'US',
        locator: 'locator0',
        materialType: MaterialTypeEnum.OfficialApiReference,
        sourceId: 'source_id2',
        textSha256: 'text_sha2564',
        title: 'title4',
        url: 'url2',
      }
    ],
    evidenceClass: 'SYNTHETIC_DEMO_SCENARIO',
    expectedRoute: 'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW',
    finalAuthority: 'PAYPAL_OR_EXTERNAL_ISSUER',
    jurisdiction: 'US',
    limitations: [
      'limitations3'
    ],
    scenarioId: 'US-DEMO-DISPUTE-EVIDENCE',
    theme: 'dispute_mediation',
    title: 'INR or counterfeit evidence organization',
  },
  schemaVersion: 1,
  source: 'local_synthetic_scenario_matcher',
  status: 'synthetic_scenarios_found',
};
```



