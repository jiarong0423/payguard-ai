# Advisory Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkFkdmlzb3J5UmVxdWVzdA

AdvisoryRequest.


# Interface Name

`AdvisoryRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `asOf` | `string` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `candidateJson` | `string` | Required | Candidate json.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8192` |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `observationMaxAgeDays` | `number` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/theme.md) | Required | Theme. |


# Example

```ts
import { AdvisoryRequest, ThemeEnum } from 'tradeglot-local-consolelib';

const advisoryRequest: AdvisoryRequest = {
  asOf: 'as_of2',
  candidateJson: 'candidate_json2',
  jurisdiction: 'US',
  observationMaxAgeDays: 220,
  theme: ThemeEnum.VelocityGuard,
};
```



