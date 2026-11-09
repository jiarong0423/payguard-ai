# State Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlN0YXRlUmVzcG9uc2U

StateResponse.


# Class Name

`StateResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `activity` | [`Activity[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/activity.md) | Required | Activity. | getActivity(): array | setActivity(array activity): void |
| `disputes` | [`DisputeSummary[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/dispute-summary.md) | Required | Disputes. | getDisputes(): array | setDisputes(array disputes): void |
| `expiresAt` | `string` | Required | Expires at. | getExpiresAt(): string | setExpiresAt(string expiresAt): void |
| `policyVersion` | `string` | Required | Policy version. | getPolicyVersion(): string | setPolicyVersion(string policyVersion): void |
| `scenario` | [`Scenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/scenario.md) | Required | Scenario. | getScenario(): Scenario | setScenario(Scenario scenario): void |
| `sessionId` | `string` | Required | Session id. | getSessionId(): string | setSessionId(string sessionId): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |
| `transactions` | [`Transaction[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/transaction.md) | Required | Transactions. | getTransactions(): array | setTransactions(array transactions): void |
| `velocity` | [`VelocityResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/velocity-response.md) | Required | VelocityResponse. | getVelocity(): VelocityResponse | setVelocity(VelocityResponse velocity): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\StateResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ActivityBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\DisputeSummaryBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\SyntheticMoneyBuilder;
use TradeGlotLocalConsoleLib\Models\Status7Enum;
use TradeGlotLocalConsoleLib\Models\Builders\ScenarioBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\TransactionBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\VelocityResponseBuilder;
use TradeGlotLocalConsoleLib\Models\BaselineProvenanceEnum;
use TradeGlotLocalConsoleLib\Models\Status14Enum;

$stateResponse = StateResponseBuilder::init(
    [
        ActivityBuilder::init(
            'at4',
            'id8',
            'kind6',
            'label8'
        )->build()
    ],
    [
        DisputeSummaryBuilder::init(
            'case_ref6',
            SyntheticMoneyBuilder::init(
                'currency_code6',
                'value0'
            )->build(),
            'opened_at0',
            'order_ref8',
            'reason2',
            'seller_response_due_date0',
            Status7Enum::NEEDS_REVIEW
        )->build()
    ],
    'expires_at6',
    'policy_version8',
    ScenarioBuilder::init(
        false,
        false
    )->build(),
    'session_id2',
    [
        TransactionBuilder::init(
            'amount0',
            'currency8',
            'occurred_at2',
            'order_id2'
        )->build()
    ],
    VelocityResponseBuilder::init(
        false,
        'baseline_amount_per_hour0',
        BaselineProvenanceEnum::SYNTHETIC_BASELINE,
        'baseline_window_end2',
        'baseline_window_start4',
        'String7',
        'current_amount_per_hour0',
        240,
        132,
        [
            'limitations7'
        ],
        'policy_version4',
        'String5',
        Status14Enum::INSUFFICIENT_BASELINE,
        'threshold4',
        'total_amount2',
        112,
        'window_end6',
        2,
        'window_start8'
    )->build()
)->build();
```



