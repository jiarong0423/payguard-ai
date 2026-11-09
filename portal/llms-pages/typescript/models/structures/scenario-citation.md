# Scenario Citation

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlNjZW5hcmlvQ2l0YXRpb24

ScenarioCitation.


# Interface Name

`ScenarioCitation`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `locator` | `string` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `materialType` | [`MaterialTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/material-type.md) | Required | Material type. |
| `sourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `textSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` |
| `url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2048` |


# Example

```ts
import {
  MaterialTypeEnum,
  ScenarioCitation,
} from 'tradeglot-local-consolelib';

const scenarioCitation: ScenarioCitation = {
  chunkId: 'chunk_id8',
  jurisdiction: 'US',
  locator: 'locator8',
  materialType: MaterialTypeEnum.OfficialApiReference,
  sourceId: 'source_id0',
  textSha256: 'text_sha2566',
  title: 'title2',
  url: 'url0',
};
```



