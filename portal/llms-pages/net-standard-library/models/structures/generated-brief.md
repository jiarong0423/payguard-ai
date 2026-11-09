# Generated Brief

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkdlbmVyYXRlZEJyaWVm

GeneratedBrief.


# Class Name

`GeneratedBrief`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CitationIds` | `List<string>` | Required | Citation ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3`, *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z0-9-]+$` |
| `EvidencePoints` | `List<string>` | Required | Evidence points.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `MissingEvidence` | `List<string>` | Required | Missing evidence.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `Summary` | `string` | Required | Summary.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1200` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;

GeneratedBrief generatedBrief = new GeneratedBrief
{
    CitationIds = new List<string>
    {
        "citation_ids9",
    },
    EvidencePoints = new List<string>
    {
        "evidence_points2",
        "evidence_points1",
    },
    MissingEvidence = new List<string>
    {
        "missing_evidence3",
        "missing_evidence4",
    },
    Summary = "summary0",
};
```



