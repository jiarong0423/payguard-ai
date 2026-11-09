# Dispute Scenario

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVTY2VuYXJpbw

DisputeScenario.


# Interface Name

`DisputeScenario`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `citations` | [`ScenarioCitation[]`](http://localhost:3000/llms-pages/typescript/models/structures/scenario-citation.md) | Required | Citations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `evidenceClass` | `string` | Required, Constant | Evidence class.<br><br>**Value**: `'SYNTHETIC_DEMO_SCENARIO'` |
| `expectedRoute` | `string` | Required, Constant | Expected route.<br><br>**Value**: `'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW'` |
| `finalAuthority` | `string` | Required, Constant | Final authority.<br><br>**Value**: `'PAYPAL_OR_EXTERNAL_ISSUER'` |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8` |
| `scenarioId` | `string` | Required, Constant | Scenario id.<br><br>**Value**: `'US-DEMO-DISPUTE-EVIDENCE'` |
| `theme` | `string` | Required, Constant | Theme.<br><br>**Value**: `'dispute_mediation'` |
| `title` | `string` | Required, Constant | Title.<br><br>**Value**: `'INR or counterfeit evidence organization'` |


# Example

```ts
import {
  DisputeScenario,
  MaterialTypeEnum,
} from 'tradeglot-local-consolelib';

const disputeScenario: DisputeScenario = {
  citations: [
    {
      chunkId: 'chunk_id0',
      jurisdiction: 'US',
      locator: 'locator0',
      materialType: MaterialTypeEnum.OfficialApiReference,
      sourceId: 'source_id2',
      textSha256: 'text_sha2564',
      title: 'title4',
      url: 'url2',
    }
  ],
  evidenceClass: 'SYNTHETIC_DEMO_SCENARIO',
  expectedRoute: 'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW',
  finalAuthority: 'PAYPAL_OR_EXTERNAL_ISSUER',
  jurisdiction: 'US',
  limitations: [
    'limitations9',
    'limitations0'
  ],
  scenarioId: 'US-DEMO-DISPUTE-EVIDENCE',
  theme: 'dispute_mediation',
  title: 'INR or counterfeit evidence organization',
};
```



