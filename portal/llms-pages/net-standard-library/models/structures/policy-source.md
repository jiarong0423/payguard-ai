# Policy Source

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlBvbGljeVNvdXJjZQ

PolicySource.


# Class Name

`PolicySource`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CitationChunkIds` | `List<string>` | Required | Citation chunk ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `29`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `ContentClass` | `string` | Required, Constant | Content class.<br><br>**Value**: `"public_reference_summary"` |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `DecisionAcceptanceDeadline` | [`PolicySourceDecisionAcceptanceDeadline`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/policy-source-decision-acceptance-deadline.md) | Required | This is a container for any-of cases. |
| `DecisionDate` | [`PolicySourceDecisionDate`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/policy-source-decision-date.md) | Required | This is a container for any-of cases. |
| `DecisionDateStatus` | [`DecisionDateStatusEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/decision-date-status.md) | Required | Decision date status. |
| `EffectiveDate` | [`PolicySourceEffectiveDate`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/policy-source-effective-date.md) | Required | This is a container for any-of cases. |
| `EffectiveDateStatus` | [`EffectiveDateStatusEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/effective-date-status.md) | Required | Effective date status. |
| `Jurisdiction` | `string` | Required | Jurisdiction.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `JurisdictionNormalized` | `string` | Required, Constant | Jurisdiction normalized.<br><br>**Value**: `"US"` |
| `MaterialType` | [`MaterialType1Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/material-type-1.md) | Required | Material type. |
| `ObservationAgeBasis` | `string` | Required, Constant | Observation age basis.<br><br>**Value**: `"saved_retrieved_at_exact_elapsed_time"` |
| `ObservationStatus` | [`ObservationStatusEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/observation-status.md) | Required | Observation status. |
| `ReasonCodes` | [`List<ReasonCode1Enum>`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `Representation` | `string` | Required, Constant | Representation.<br><br>**Value**: `"authored_paraphrase_not_full_source"` |
| `RetrievedAt` | `string` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `SourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `SourceUpdatedDate` | [`PolicySourceSourceUpdatedDate`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/policy-source-source-updated-date.md) | Required | This is a container for any-of cases. |
| `SourceUpdatedDateStatus` | [`SourceUpdatedDateStatusEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. |
| `Title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `Url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

PolicySource policySource = new PolicySource
{
    CitationChunkIds = new List<string>
    {
        "citation_chunk_ids4",
    },
    ContentClass = "public_reference_summary",
    CurrentPolicyApplicability = "NOT_ESTABLISHED",
    DecisionAcceptanceDeadline = PolicySourceDecisionAcceptanceDeadline.FromString("String7"),
    DecisionDate = PolicySourceDecisionDate.FromString("String1"),
    DecisionDateStatus = DecisionDateStatusEnum.NOTAPPLICABLE,
    EffectiveDate = PolicySourceEffectiveDate.FromString("String3"),
    EffectiveDateStatus = EffectiveDateStatusEnum.DOCUMENTSTATED,
    Jurisdiction = "jurisdiction2",
    JurisdictionNormalized = "US",
    MaterialType = MaterialType1Enum.OfficialApiReference,
    ObservationAgeBasis = "saved_retrieved_at_exact_elapsed_time",
    ObservationStatus = ObservationStatusEnum.STALEOBSERVATION,
    ReasonCodes = new List<ReasonCode1Enum>
    {
        ReasonCode1Enum.STALEOBSERVATION,
    },
    Representation = "authored_paraphrase_not_full_source",
    RetrievedAt = "retrieved_at2",
    SourceId = "source_id2",
    SourceUpdatedDate = PolicySourceSourceUpdatedDate.FromString("String1"),
    SourceUpdatedDateStatus = SourceUpdatedDateStatusEnum.DOCUMENTSTATED,
    Title = "title6",
    Url = "url2",
};
```



