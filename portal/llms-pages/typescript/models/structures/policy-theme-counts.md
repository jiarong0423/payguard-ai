# Policy Theme Counts

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlBvbGljeVRoZW1lQ291bnRz

PolicyThemeCounts.


# Interface Name

`PolicyThemeCounts`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `disputeMediation` | `number` | Required | Dispute mediation.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `sourceCompliance` | `number` | Required | Source compliance.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `velocityGuard` | `number` | Required | Velocity guard.<br><br>**Constraints**: `>= 0`, `<= 29` |


# Example

```ts
import { PolicyThemeCounts } from 'tradeglot-local-consolelib';

const policyThemeCounts: PolicyThemeCounts = {
  disputeMediation: 29,
  sourceCompliance: 29,
  velocityGuard: 29,
};
```



