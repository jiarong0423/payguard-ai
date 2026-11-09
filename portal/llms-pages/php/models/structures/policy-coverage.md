# Policy Coverage

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlBvbGljeUNvdmVyYWdl

PolicyCoverage.


# Class Name

`PolicyCoverage`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `basis` | `string` | Required, Constant | Basis.<br><br>**Value**: `'pinned_authored_summaries_only'` | getBasis(): string | setBasis(string basis): void |
| `complete` | `bool` | Required | Complete. | getComplete(): bool | setComplete(bool complete): void |
| `missingOfficialPolicyThemes` | [`string(MissingOfficialPolicyThemeEnum)[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/missing-official-policy-theme.md) | Required | Missing official policy themes.<br><br>**Constraints**: *Maximum Items*: `3` | getMissingOfficialPolicyThemes(): array | setMissingOfficialPolicyThemes(array missingOfficialPolicyThemes): void |
| `officialPolicyChunkCountByTheme` | [`PolicyThemeCounts`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/policy-theme-counts.md) | Required | PolicyThemeCounts. | getOfficialPolicyChunkCountByTheme(): PolicyThemeCounts | setOfficialPolicyChunkCountByTheme(PolicyThemeCounts officialPolicyChunkCountByTheme): void |
| `officialPolicySourceIds` | `string[]` | Required | Official policy source ids.<br><br>**Constraints**: *Maximum Items*: `16`, *Pattern*: `^[A-Z0-9-]{1,128}$` | getOfficialPolicySourceIds(): array | setOfficialPolicySourceIds(array officialPolicySourceIds): void |
| `regionalSourceCount` | `int` | Required | Regional source count.<br><br>**Constraints**: `>= 0`, `<= 16` | getRegionalSourceCount(): int | setRegionalSourceCount(int regionalSourceCount): void |
| `selectedChunkCount` | `int` | Required | Selected chunk count.<br><br>**Constraints**: `>= 0`, `<= 29` | getSelectedChunkCount(): int | setSelectedChunkCount(int selectedChunkCount): void |
| `selectedSourceCount` | `int` | Required | Selected source count.<br><br>**Constraints**: `>= 0`, `<= 16` | getSelectedSourceCount(): int | setSelectedSourceCount(int selectedSourceCount): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\PolicyCoverageBuilder;
use TradeGlotLocalConsoleLib\Models\MissingOfficialPolicyThemeEnum;
use TradeGlotLocalConsoleLib\Models\Builders\PolicyThemeCountsBuilder;

$policyCoverage = PolicyCoverageBuilder::init(
    false,
    [
        MissingOfficialPolicyThemeEnum::SOURCE_COMPLIANCE
    ],
    PolicyThemeCountsBuilder::init(
        12,
        29,
        29
    )->build(),
    [
        'official_policy_source_ids0'
    ],
    16,
    29,
    16
)->build();
```



