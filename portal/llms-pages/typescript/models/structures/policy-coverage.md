# Policy Coverage

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlBvbGljeUNvdmVyYWdl

PolicyCoverage.


# Interface Name

`PolicyCoverage`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `basis` | `string` | Required, Constant | Basis.<br><br>**Value**: `'pinned_authored_summaries_only'` |
| `complete` | `boolean` | Required | Complete. |
| `missingOfficialPolicyThemes` | [`MissingOfficialPolicyThemeEnum[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/missing-official-policy-theme.md) | Required | Missing official policy themes.<br><br>**Constraints**: *Maximum Items*: `3` |
| `officialPolicyChunkCountByTheme` | [`PolicyThemeCounts`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/policy-theme-counts.md) | Required | PolicyThemeCounts. |
| `officialPolicySourceIds` | `string[]` | Required | Official policy source ids.<br><br>**Constraints**: *Maximum Items*: `16`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `regionalSourceCount` | `number` | Required | Regional source count.<br><br>**Constraints**: `>= 0`, `<= 16` |
| `selectedChunkCount` | `number` | Required | Selected chunk count.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `selectedSourceCount` | `number` | Required | Selected source count.<br><br>**Constraints**: `>= 0`, `<= 16` |


# Example

```ts
import {
  MissingOfficialPolicyThemeEnum,
  PolicyCoverage,
} from 'tradeglot-local-consolelib';

const policyCoverage: PolicyCoverage = {
  basis: 'pinned_authored_summaries_only',
  complete: false,
  missingOfficialPolicyThemes: [
    MissingOfficialPolicyThemeEnum.SourceCompliance
  ],
  officialPolicyChunkCountByTheme: {
    disputeMediation: 12,
    sourceCompliance: 29,
    velocityGuard: 29,
  },
  officialPolicySourceIds: [
    'official_policy_source_ids0'
  ],
  regionalSourceCount: 16,
  selectedChunkCount: 29,
  selectedSourceCount: 16,
};
```



