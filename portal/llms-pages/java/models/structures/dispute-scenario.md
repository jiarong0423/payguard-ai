# Dispute Scenario

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVTY2VuYXJpbw

DisputeScenario.


# Class Name

`DisputeScenario`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Citations` | [`List<ScenarioCitation>`](http://localhost:3000/llms-pages/java/models/structures/scenario-citation.md) | Required | Citations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` | List<ScenarioCitation> getCitations() | setCitations(List<ScenarioCitation> citations) |
| `EvidenceClass` | `String` | Required, Constant | Evidence class.<br><br>**Value**: `"SYNTHETIC_DEMO_SCENARIO"` | String getEvidenceClass() | setEvidenceClass(String evidenceClass) |
| `ExpectedRoute` | `String` | Required, Constant | Expected route.<br><br>**Value**: `"PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW"` | String getExpectedRoute() | setExpectedRoute(String expectedRoute) |
| `FinalAuthority` | `String` | Required, Constant | Final authority.<br><br>**Value**: `"PAYPAL_OR_EXTERNAL_ISSUER"` | String getFinalAuthority() | setFinalAuthority(String finalAuthority) |
| `Jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` | String getJurisdiction() | setJurisdiction(String jurisdiction) |
| `Limitations` | `List<String>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8` | List<String> getLimitations() | setLimitations(List<String> limitations) |
| `ScenarioId` | `String` | Required, Constant | Scenario id.<br><br>**Value**: `"US-DEMO-DISPUTE-EVIDENCE"` | String getScenarioId() | setScenarioId(String scenarioId) |
| `Theme` | `String` | Required, Constant | Theme.<br><br>**Value**: `"dispute_mediation"` | String getTheme() | setTheme(String theme) |
| `Title` | `String` | Required, Constant | Title.<br><br>**Value**: `"INR or counterfeit evidence organization"` | String getTitle() | setTitle(String title) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.DisputeScenario;
import m18000.m0.m0.m127.models.MaterialTypeEnum;
import m18000.m0.m0.m127.models.ScenarioCitation;

DisputeScenario disputeScenario = new DisputeScenario.Builder(
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
        "limitations9",
        "limitations0"
    ),
    "US-DEMO-DISPUTE-EVIDENCE",
    "dispute_mediation",
    "INR or counterfeit evidence organization"
)
.build();
```



