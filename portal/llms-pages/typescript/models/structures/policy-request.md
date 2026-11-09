# Policy Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlBvbGljeVJlcXVlc3Q

PolicyRequest.


# Interface Name

`PolicyRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `asOf` | `string` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `observationMaxAgeDays` | `number` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/theme.md) | Required | Theme. |


# Example

```ts
import { PolicyRequest, ThemeEnum } from 'tradeglot-local-consolelib';

const policyRequest: PolicyRequest = {
  asOf: 'as_of8',
  jurisdiction: 'US',
  observationMaxAgeDays: 186,
  theme: ThemeEnum.DisputeMediation,
};
```



