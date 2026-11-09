# Generated Brief

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkdlbmVyYXRlZEJyaWVm

GeneratedBrief.


# Class Name

`GeneratedBrief`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `citationIds` | `string[]` | Required | Citation ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3`, *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z0-9-]+$` | getCitationIds(): array | setCitationIds(array citationIds): void |
| `evidencePoints` | `string[]` | Required | Evidence points.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` | getEvidencePoints(): array | setEvidencePoints(array evidencePoints): void |
| `missingEvidence` | `string[]` | Required | Missing evidence.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` | getMissingEvidence(): array | setMissingEvidence(array missingEvidence): void |
| `summary` | `string` | Required | Summary.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1200` | getSummary(): string | setSummary(string summary): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GeneratedBriefBuilder;

$generatedBrief = GeneratedBriefBuilder::init(
    [
        'citation_ids9'
    ],
    [
        'evidence_points2',
        'evidence_points1'
    ],
    [
        'missing_evidence3',
        'missing_evidence4'
    ],
    'summary0'
)->build();
```



