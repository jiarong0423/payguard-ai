# Aup Acknowledge Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVzcG9uc2U

AupAcknowledgeResponse.


# Class Name

`AupAcknowledgeResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `acknowledgementToken` | string | Required | This is a container for any-of cases. | getAcknowledgementToken(): string | setAcknowledgementToken(string acknowledgementToken): void |
| `choice` | [`string(ChoiceEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/choice.md) | Required | Choice. | getChoice(): string | setChoice(string choice): void |
| `complianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `'NOT_MADE'` | getComplianceDecision(): string | setComplianceDecision(string complianceDecision): void |
| `descriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getDescriptionDigest(): string | setDescriptionDigest(string descriptionDigest): void |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | getEvaluationId(): string | setEvaluationId(string evaluationId): void |
| `expiresAt` | string | Required | This is a container for any-of cases. | getExpiresAt(): string | setExpiresAt(string expiresAt): void |
| `externalActionAuthorized` | `string` | Required, Constant | External action authorized.<br><br>**Value**: `'False'` | getExternalActionAuthorized(): string | setExternalActionAuthorized(string externalActionAuthorized): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |
| `warningCopyVersion` | `string` | Required, Constant | Warning copy version.<br><br>**Value**: `'aup-warning-v1'` | getWarningCopyVersion(): string | setWarningCopyVersion(string warningCopyVersion): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AupAcknowledgeResponseBuilder;
use TradeGlotLocalConsoleLib\Models\ChoiceEnum;

$aupAcknowledgeResponse = AupAcknowledgeResponseBuilder::init(
    'String9',
    ChoiceEnum::ACKNOWLEDGE_AND_CONTINUE,
    'description_digest6',
    'evaluation_id2',
    'String9'
)->build();
```



