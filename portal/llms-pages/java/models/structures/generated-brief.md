# Generated Brief

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkdlbmVyYXRlZEJyaWVm

GeneratedBrief.


# Class Name

`GeneratedBrief`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CitationIds` | `List<String>` | Required | Citation ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3`, *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z0-9-]+$` | List<String> getCitationIds() | setCitationIds(List<String> citationIds) |
| `EvidencePoints` | `List<String>` | Required | Evidence points.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` | List<String> getEvidencePoints() | setEvidencePoints(List<String> evidencePoints) |
| `MissingEvidence` | `List<String>` | Required | Missing evidence.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` | List<String> getMissingEvidence() | setMissingEvidence(List<String> missingEvidence) |
| `Summary` | `String` | Required | Summary.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1200` | String getSummary() | setSummary(String summary) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.GeneratedBrief;

GeneratedBrief generatedBrief = new GeneratedBrief.Builder(
    Arrays.asList(
        "citation_ids9"
    ),
    Arrays.asList(
        "evidence_points2",
        "evidence_points1"
    ),
    Arrays.asList(
        "missing_evidence3",
        "missing_evidence4"
    ),
    "summary0"
)
.build();
```



