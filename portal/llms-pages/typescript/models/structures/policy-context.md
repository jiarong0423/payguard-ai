# Policy Context

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlBvbGljeUNvbnRleHQ

PolicyContext.


# Interface Name

`PolicyContext`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `asOf` | `string` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `observationMaxAgeDays` | `number` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/theme.md) | Required | Theme. |


# Example

```ts
import { PolicyContext, ThemeEnum } from 'tradeglot-local-consolelib';

const policyContext: PolicyContext = {
  asOf: 'as_of4',
  jurisdiction: 'US',
  observationMaxAgeDays: 12,
  theme: ThemeEnum.VelocityGuard,
};
```



