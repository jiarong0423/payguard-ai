# Scenario Match

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlNjZW5hcmlvTWF0Y2g

ScenarioMatch.


# Class Name

`ScenarioMatch`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CurrentPolicyApplicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` | String getCurrentPolicyApplicability() | setCurrentPolicyApplicability(String currentPolicyApplicability) |
| `EngineExecution` | `String` | Required, Constant | Engine execution.<br><br>**Value**: `"NOT_RUN"` | String getEngineExecution() | setEngineExecution(String engineExecution) |
| `EvaluationScope` | `String` | Required, Constant | Evaluation scope.<br><br>**Value**: `"AUTHORED_SYNTHETIC_DEMO_ONLY"` | String getEvaluationScope() | setEvaluationScope(String evaluationScope) |
| `IntakeStatus` | [`IntakeStatusEnum`](http://localhost:3000/llms-pages/java/models/enumerations/intake-status.md) | Required | Intake status. | IntakeStatusEnum getIntakeStatus() | setIntakeStatus(IntakeStatusEnum intakeStatus) |
| `OperationalAuthority` | `String` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` | String getOperationalAuthority() | setOperationalAuthority(String operationalAuthority) |
| `Provenance` | `String` | Required, Constant | Provenance.<br><br>**Value**: `"AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES"` | String getProvenance() | setProvenance(String provenance) |
| `RealCaseEvidence` | `String` | Required, Constant | Real case evidence.<br><br>**Value**: `"NOT_PROVIDED"` | String getRealCaseEvidence() | setRealCaseEvidence(String realCaseEvidence) |
| `RequiredHumanReview` | `String` | Required, Constant | Required human review.<br><br>**Value**: `"True"` | String getRequiredHumanReview() | setRequiredHumanReview(String requiredHumanReview) |
| `Scenario` | [`DisputeScenario`](http://localhost:3000/llms-pages/java/models/structures/dispute-scenario.md) | Required | DisputeScenario. | DisputeScenario getScenario() | setScenario(DisputeScenario scenario) |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | int getSchemaVersion() | setSchemaVersion(int schemaVersion) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"local_synthetic_scenario_matcher"` | String getSource() | setSource(String source) |
| `Status` | `String` | Required, Constant | Status.<br><br>**Value**: `"synthetic_scenarios_found"` | String getStatus() | setStatus(String status) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.DisputeScenario;
import m18000.m0.m0.m127.models.IntakeStatusEnum;
import m18000.m0.m0.m127.models.MaterialTypeEnum;
import m18000.m0.m0.m127.models.ScenarioCitation;
import m18000.m0.m0.m127.models.ScenarioMatch;

ScenarioMatch scenarioMatch = new ScenarioMatch.Builder(
    "NOT_ESTABLISHED",
    "NOT_RUN",
    "AUTHORED_SYNTHETIC_DEMO_ONLY",
    IntakeStatusEnum.READY_FOR_LOCAL_RULES,
    "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
    "AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES",
    "NOT_PROVIDED",
    "True",
    new DisputeScenario.Builder(
        Arrays.asList(
            new ScenarioCitation.Builder(
                "chunk_id0",
                "US",
                "locator0",
                MaterialTypeEnum.OFFICIAL_API_REFERENCE,
                "source_id2",
                "text_sha2564",
                "title4",
                "url2"
            )
            .build()
        ),
        "SYNTHETIC_DEMO_SCENARIO",
        "PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW",
        "PAYPAL_OR_EXTERNAL_ISSUER",
        "US",
        Arrays.asList(
            "limitations3"
        ),
        "US-DEMO-DISPUTE-EVIDENCE",
        "dispute_mediation",
        "INR or counterfeit evidence organization"
    )
    .build(),
    1,
    "local_synthetic_scenario_matcher",
    "synthetic_scenarios_found"
)
.build();
```



