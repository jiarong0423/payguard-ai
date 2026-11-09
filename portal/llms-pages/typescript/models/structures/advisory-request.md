# Advisory Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFkdmlzb3J5UmVxdWVzdA

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
| `theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/theme.md) | Required | Theme. |


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



