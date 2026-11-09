# Policy Source

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlBvbGljeVNvdXJjZQ

PolicySource.


# Class Name

`PolicySource`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CitationChunkIds` | `[]string` | Required | Citation chunk ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `29`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `ContentClass` | `string` | Required, Constant | Content class.<br><br>**Value**: `"public_reference_summary"` |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `DecisionAcceptanceDeadline` | [`models.PolicySourceDecisionAcceptanceDeadline`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/policy-source-decision-acceptance-deadline.md) | Required | This is a container for any-of cases. |
| `DecisionDate` | [`models.PolicySourceDecisionDate`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/policy-source-decision-date.md) | Required | This is a container for any-of cases. |
| `DecisionDateStatus` | [`models.DecisionDateStatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/decision-date-status.md) | Required | Decision date status. |
| `EffectiveDate` | [`models.PolicySourceEffectiveDate`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/policy-source-effective-date.md) | Required | This is a container for any-of cases. |
| `EffectiveDateStatus` | [`models.EffectiveDateStatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/effective-date-status.md) | Required | Effective date status. |
| `Jurisdiction` | `string` | Required | Jurisdiction.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `JurisdictionNormalized` | `string` | Required, Constant | Jurisdiction normalized.<br><br>**Value**: `"US"` |
| `MaterialType` | [`models.MaterialType1Enum`](http://localhost:3000/llms-pages/go/models/enumerations/material-type-1.md) | Required | Material type. |
| `ObservationAgeBasis` | `string` | Required, Constant | Observation age basis.<br><br>**Value**: `"saved_retrieved_at_exact_elapsed_time"` |
| `ObservationStatus` | [`models.ObservationStatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/observation-status.md) | Required | Observation status. |
| `ReasonCodes` | [`[]models.ReasonCode1Enum`](http://localhost:3000/llms-pages/go/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `Representation` | `string` | Required, Constant | Representation.<br><br>**Value**: `"authored_paraphrase_not_full_source"` |
| `RetrievedAt` | `string` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `SourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `SourceUpdatedDate` | [`models.PolicySourceSourceUpdatedDate`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/policy-source-source-updated-date.md) | Required | This is a container for any-of cases. |
| `SourceUpdatedDateStatus` | [`models.SourceUpdatedDateStatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. |
| `Title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `Url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    policySource := models.PolicySource{
        CitationChunkIds:           []string{
            "citation_chunk_ids4",
        },
        ContentClass:               "public_reference_summary",
        CurrentPolicyApplicability: "NOT_ESTABLISHED",
        DecisionAcceptanceDeadline: models.PolicySourceDecisionAcceptanceDeadlineContainer.FromString("String7"),
        DecisionDate:               models.PolicySourceDecisionDateContainer.FromString("String1"),
        DecisionDateStatus:         models.DecisionDateStatusEnum_NOTAPPLICABLE,
        EffectiveDate:              models.PolicySourceEffectiveDateContainer.FromString("String3"),
        EffectiveDateStatus:        models.EffectiveDateStatusEnum_DOCUMENTSTATED,
        Jurisdiction:               "jurisdiction2",
        JurisdictionNormalized:     "US",
        MaterialType:               models.MaterialType1Enum_OFFICIALAPIREFERENCE,
        ObservationAgeBasis:        "saved_retrieved_at_exact_elapsed_time",
        ObservationStatus:          models.ObservationStatusEnum_STALEOBSERVATION,
        ReasonCodes:                []models.ReasonCode1Enum{
            models.ReasonCode1Enum_STALEOBSERVATION,
        },
        Representation:             "authored_paraphrase_not_full_source",
        RetrievedAt:                "retrieved_at2",
        SourceId:                   "source_id2",
        SourceUpdatedDate:          models.PolicySourceSourceUpdatedDateContainer.FromString("String1"),
        SourceUpdatedDateStatus:    models.SourceUpdatedDateStatusEnum_DOCUMENTSTATED,
        Title:                      "title6",
        Url:                        "url2",
    }

}
```



