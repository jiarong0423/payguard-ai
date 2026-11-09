# Aup Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkF1cFJlc3BvbnNl

AupResponse.


# Class Name

`AupResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` | getAdvisoryOnly(): string | setAdvisoryOnly(string advisoryOnly): void |
| `complianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `'NOT_MADE'` | getComplianceDecision(): string | setComplianceDecision(string complianceDecision): void |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` | getCurrentPolicyApplicability(): string | setCurrentPolicyApplicability(string currentPolicyApplicability): void |
| `descriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getDescriptionDigest(): string | setDescriptionDigest(string descriptionDigest): void |
| `evaluatedAt` | `string` | Required | Evaluated at. | getEvaluatedAt(): string | setEvaluatedAt(string evaluatedAt): void |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | getEvaluationId(): string | setEvaluationId(string evaluationId): void |
| `expiresAt` | `string` | Required | Expires at. | getExpiresAt(): string | setExpiresAt(string expiresAt): void |
| `findings` | [`Finding[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/finding.md) | Required | Findings. | getFindings(): array | setFindings(array findings): void |
| `matchStatus` | [`string(MatchStatusEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/match-status.md) | Required | Match status. | getMatchStatus(): string | setMatchStatus(string matchStatus): void |
| `policyUrl` | `string` | Required, Constant | Policy url.<br><br>**Value**: `'https://www.paypal.com/us/legalhub/paypal/acceptableuse-full'` | getPolicyUrl(): string | setPolicyUrl(string policyUrl): void |
| `policyVersion` | `string` | Required | Policy version.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` | getPolicyVersion(): string | setPolicyVersion(string policyVersion): void |
| `recommendation` | `string` | Required | Recommendation.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` | getRecommendation(): string | setRecommendation(string recommendation): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |
| `warningCopyVersion` | `string` | Required, Constant | Warning copy version.<br><br>**Value**: `'aup-warning-v1'` | getWarningCopyVersion(): string | setWarningCopyVersion(string warningCopyVersion): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AupResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\FindingBuilder;
use TradeGlotLocalConsoleLib\Models\CategoryEnum;
use TradeGlotLocalConsoleLib\Models\MatchStatusEnum;

$aupResponse = AupResponseBuilder::init(
    'description_digest8',
    'evaluated_at4',
    'evaluation_id4',
    'expires_at4',
    [
        FindingBuilder::init(
            CategoryEnum::WEAPONS
        )->build()
    ],
    MatchStatusEnum::NO_MATCH,
    'policy_version8',
    'recommendation6'
)->build();
```



