# Scenario Match

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlNjZW5hcmlvTWF0Y2g

ScenarioMatch.


# Class Name

`ScenarioMatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `current_policy_applicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `engine_execution` | `String` | Required, Constant | Engine execution.<br><br>**Value**: `'NOT_RUN'` |
| `evaluation_scope` | `String` | Required, Constant | Evaluation scope.<br><br>**Value**: `'AUTHORED_SYNTHETIC_DEMO_ONLY'` |
| `intake_status` | [`IntakeStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/intake-status.md) | Required | Intake status. |
| `operational_authority` | `String` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` |
| `provenance` | `String` | Required, Constant | Provenance.<br><br>**Value**: `'AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES'` |
| `real_case_evidence` | `String` | Required, Constant | Real case evidence.<br><br>**Value**: `'NOT_PROVIDED'` |
| `required_human_review` | `String` | Required, Constant | Required human review.<br><br>**Value**: `'True'` |
| `scenario` | [`DisputeScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/dispute-scenario.md) | Required | DisputeScenario. |
| `schema_version` | `Integer` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'local_synthetic_scenario_matcher'` |
| `status` | `String` | Required, Constant | Status.<br><br>**Value**: `'synthetic_scenarios_found'` |


# Example

```ruby
scenario_match = ScenarioMatch.new(
  'NOT_ESTABLISHED',
  'NOT_RUN',
  'AUTHORED_SYNTHETIC_DEMO_ONLY',
  IntakeStatusEnum::READY_FOR_LOCAL_RULES,
  'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  'AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES',
  'NOT_PROVIDED',
  'True',
  DisputeScenario.new(
    [
      ScenarioCitation.new(
        'chunk_id0',
        'US',
        'locator0',
        MaterialTypeEnum::OFFICIAL_API_REFERENCE,
        'source_id2',
        'text_sha2564',
        'title4',
        'url2'
      )
    ],
    'SYNTHETIC_DEMO_SCENARIO',
    'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW',
    'PAYPAL_OR_EXTERNAL_ISSUER',
    'US',
    [
      'limitations3'
    ],
    'US-DEMO-DISPUTE-EVIDENCE',
    'dispute_mediation',
    'INR or counterfeit evidence organization'
  ),
  1,
  'local_synthetic_scenario_matcher',
  'synthetic_scenarios_found'
)
```



