# Dispute Scenario

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVTY2VuYXJpbw

DisputeScenario.


# Class Name

`DisputeScenario`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Citations` | [`[]models.ScenarioCitation`](http://localhost:3000/llms-pages/go/models/structures/scenario-citation.md) | Required | Citations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `EvidenceClass` | `string` | Required, Constant | Evidence class.<br><br>**Value**: `"SYNTHETIC_DEMO_SCENARIO"` |
| `ExpectedRoute` | `string` | Required, Constant | Expected route.<br><br>**Value**: `"PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW"` |
| `FinalAuthority` | `string` | Required, Constant | Final authority.<br><br>**Value**: `"PAYPAL_OR_EXTERNAL_ISSUER"` |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `Limitations` | `[]string` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8` |
| `ScenarioId` | `string` | Required, Constant | Scenario id.<br><br>**Value**: `"US-DEMO-DISPUTE-EVIDENCE"` |
| `Theme` | `string` | Required, Constant | Theme.<br><br>**Value**: `"dispute_mediation"` |
| `Title` | `string` | Required, Constant | Title.<br><br>**Value**: `"INR or counterfeit evidence organization"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    disputeScenario := models.DisputeScenario{
        Citations:      []models.ScenarioCitation{
            models.ScenarioCitation{
                ChunkId:      "chunk_id0",
                Jurisdiction: "US",
                Locator:      "locator0",
                MaterialType: models.MaterialTypeEnum_OFFICIALAPIREFERENCE,
                SourceId:     "source_id2",
                TextSha256:   "text_sha2564",
                Title:        "title4",
                Url:          "url2",
            },
        },
        EvidenceClass:  "SYNTHETIC_DEMO_SCENARIO",
        ExpectedRoute:  "PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW",
        FinalAuthority: "PAYPAL_OR_EXTERNAL_ISSUER",
        Jurisdiction:   "US",
        Limitations:    []string{
            "limitations9",
            "limitations0",
        },
        ScenarioId:     "US-DEMO-DISPUTE-EVIDENCE",
        Theme:          "dispute_mediation",
        Title:          "INR or counterfeit evidence organization",
    }

}
```



