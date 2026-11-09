# Scenario Match

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlNjZW5hcmlvTWF0Y2g

ScenarioMatch.


# Class Name

`ScenarioMatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `EngineExecution` | `string` | Required, Constant | Engine execution.<br><br>**Value**: `"NOT_RUN"` |
| `EvaluationScope` | `string` | Required, Constant | Evaluation scope.<br><br>**Value**: `"AUTHORED_SYNTHETIC_DEMO_ONLY"` |
| `IntakeStatus` | [`IntakeStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/intake-status.md) | Required | Intake status. |
| `OperationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `Provenance` | `string` | Required, Constant | Provenance.<br><br>**Value**: `"AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES"` |
| `RealCaseEvidence` | `string` | Required, Constant | Real case evidence.<br><br>**Value**: `"NOT_PROVIDED"` |
| `RequiredHumanReview` | `string` | Required, Constant | Required human review.<br><br>**Value**: `"True"` |
| `Scenario` | [`DisputeScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/dispute-scenario.md) | Required | DisputeScenario. |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"local_synthetic_scenario_matcher"` |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"synthetic_scenarios_found"` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;

ScenarioMatch scenarioMatch = new ScenarioMatch
{
    CurrentPolicyApplicability = "NOT_ESTABLISHED",
    EngineExecution = "NOT_RUN",
    EvaluationScope = "AUTHORED_SYNTHETIC_DEMO_ONLY",
    IntakeStatus = IntakeStatusEnum.ReadyForLocalRules,
    OperationalAuthority = "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
    Provenance = "AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES",
    RealCaseEvidence = "NOT_PROVIDED",
    RequiredHumanReview = "True",
    Scenario = new DisputeScenario
    {
        Citations = new List<ScenarioCitation>
        {
            new ScenarioCitation
            {
                ChunkId = "chunk_id0",
                Jurisdiction = "US",
                Locator = "locator0",
                MaterialType = MaterialTypeEnum.OfficialApiReference,
                SourceId = "source_id2",
                TextSha256 = "text_sha2564",
                Title = "title4",
                Url = "url2",
            },
        },
        EvidenceClass = "SYNTHETIC_DEMO_SCENARIO",
        ExpectedRoute = "PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW",
        FinalAuthority = "PAYPAL_OR_EXTERNAL_ISSUER",
        Jurisdiction = "US",
        Limitations = new List<string>
        {
            "limitations3",
        },
        ScenarioId = "US-DEMO-DISPUTE-EVIDENCE",
        Theme = "dispute_mediation",
        Title = "INR or counterfeit evidence organization",
    },
    SchemaVersion = 1,
    Source = "local_synthetic_scenario_matcher",
    Status = "synthetic_scenarios_found",
};
```



