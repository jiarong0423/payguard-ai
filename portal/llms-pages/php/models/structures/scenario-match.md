# Scenario Match

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlNjZW5hcmlvTWF0Y2g

ScenarioMatch.


# Class Name

`ScenarioMatch`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` | getCurrentPolicyApplicability(): string | setCurrentPolicyApplicability(string currentPolicyApplicability): void |
| `engineExecution` | `string` | Required, Constant | Engine execution.<br><br>**Value**: `'NOT_RUN'` | getEngineExecution(): string | setEngineExecution(string engineExecution): void |
| `evaluationScope` | `string` | Required, Constant | Evaluation scope.<br><br>**Value**: `'AUTHORED_SYNTHETIC_DEMO_ONLY'` | getEvaluationScope(): string | setEvaluationScope(string evaluationScope): void |
| `intakeStatus` | [`string(IntakeStatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/intake-status.md) | Required | Intake status. | getIntakeStatus(): string | setIntakeStatus(string intakeStatus): void |
| `operationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` | getOperationalAuthority(): string | setOperationalAuthority(string operationalAuthority): void |
| `provenance` | `string` | Required, Constant | Provenance.<br><br>**Value**: `'AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES'` | getProvenance(): string | setProvenance(string provenance): void |
| `realCaseEvidence` | `string` | Required, Constant | Real case evidence.<br><br>**Value**: `'NOT_PROVIDED'` | getRealCaseEvidence(): string | setRealCaseEvidence(string realCaseEvidence): void |
| `requiredHumanReview` | `string` | Required, Constant | Required human review.<br><br>**Value**: `'True'` | getRequiredHumanReview(): string | setRequiredHumanReview(string requiredHumanReview): void |
| `scenario` | [`DisputeScenario`](http://localhost:3000/llms-pages/php/models/structures/dispute-scenario.md) | Required | DisputeScenario. | getScenario(): DisputeScenario | setScenario(DisputeScenario scenario): void |
| `schemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | getSchemaVersion(): int | setSchemaVersion(int schemaVersion): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'local_synthetic_scenario_matcher'` | getSource(): string | setSource(string source): void |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'synthetic_scenarios_found'` | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ScenarioMatchBuilder;
use TradeGlotLocalConsoleLib\Models\IntakeStatusEnum;
use TradeGlotLocalConsoleLib\Models\Builders\DisputeScenarioBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ScenarioCitationBuilder;
use TradeGlotLocalConsoleLib\Models\MaterialTypeEnum;

$scenarioMatch = ScenarioMatchBuilder::init(
    IntakeStatusEnum::READY_FOR_LOCAL_RULES,
    DisputeScenarioBuilder::init(
        [
            ScenarioCitationBuilder::init(
                'chunk_id0',
                'locator0',
                MaterialTypeEnum::OFFICIAL_API_REFERENCE,
                'source_id2',
                'text_sha2564',
                'title4',
                'url2'
            )->build()
        ],
        [
            'limitations3'
        ]
    )->build()
)->build();
```



