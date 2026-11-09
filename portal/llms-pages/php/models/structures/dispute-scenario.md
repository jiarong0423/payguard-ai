# Dispute Scenario

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVTY2VuYXJpbw

DisputeScenario.


# Class Name

`DisputeScenario`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `citations` | [`ScenarioCitation[]`](http://localhost:3000/llms-pages/php/models/structures/scenario-citation.md) | Required | Citations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` | getCitations(): array | setCitations(array citations): void |
| `evidenceClass` | `string` | Required, Constant | Evidence class.<br><br>**Value**: `'SYNTHETIC_DEMO_SCENARIO'` | getEvidenceClass(): string | setEvidenceClass(string evidenceClass): void |
| `expectedRoute` | `string` | Required, Constant | Expected route.<br><br>**Value**: `'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW'` | getExpectedRoute(): string | setExpectedRoute(string expectedRoute): void |
| `finalAuthority` | `string` | Required, Constant | Final authority.<br><br>**Value**: `'PAYPAL_OR_EXTERNAL_ISSUER'` | getFinalAuthority(): string | setFinalAuthority(string finalAuthority): void |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8` | getLimitations(): array | setLimitations(array limitations): void |
| `scenarioId` | `string` | Required, Constant | Scenario id.<br><br>**Value**: `'US-DEMO-DISPUTE-EVIDENCE'` | getScenarioId(): string | setScenarioId(string scenarioId): void |
| `theme` | `string` | Required, Constant | Theme.<br><br>**Value**: `'dispute_mediation'` | getTheme(): string | setTheme(string theme): void |
| `title` | `string` | Required, Constant | Title.<br><br>**Value**: `'INR or counterfeit evidence organization'` | getTitle(): string | setTitle(string title): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeScenarioBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ScenarioCitationBuilder;
use TradeGlotLocalConsoleLib\Models\MaterialTypeEnum;

$disputeScenario = DisputeScenarioBuilder::init(
    [
        ScenarioCitationBuilder::init(
            'chunk_id0',
            'locator0',
            MaterialTypeEnum::OFFICIAL_API_REFERENCE,
            'source_id2',
            'text_sha2564',
            'title4',
            'url2'
        )->build()
    ],
    [
        'limitations9',
        'limitations0'
    ]
)->build();
```



