# Generated Brief

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkdlbmVyYXRlZEJyaWVm

GeneratedBrief.


# Interface Name

`GeneratedBrief`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `citationIds` | `string[]` | Required | Citation ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3`, *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z0-9-]+$` |
| `evidencePoints` | `string[]` | Required | Evidence points.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `missingEvidence` | `string[]` | Required | Missing evidence.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `summary` | `string` | Required | Summary.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1200` |


# Example

```ts
import { GeneratedBrief } from 'tradeglot-local-consolelib';

const generatedBrief: GeneratedBrief = {
  citationIds: [
    'citation_ids9'
  ],
  evidencePoints: [
    'evidence_points2',
    'evidence_points1'
  ],
  missingEvidence: [
    'missing_evidence3',
    'missing_evidence4'
  ],
  summary: 'summary0',
};
```



