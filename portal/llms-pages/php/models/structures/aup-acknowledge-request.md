# Aup Acknowledge Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVxdWVzdA

AupAcknowledgeRequest.


# Class Name

`AupAcknowledgeRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `choice` | [`string(ChoiceEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/choice.md) | Required | Choice. | getChoice(): string | setChoice(string choice): void |
| `descriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getDescriptionDigest(): string | setDescriptionDigest(string descriptionDigest): void |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | getEvaluationId(): string | setEvaluationId(string evaluationId): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AupAcknowledgeRequestBuilder;
use TradeGlotLocalConsoleLib\Models\ChoiceEnum;

$aupAcknowledgeRequest = AupAcknowledgeRequestBuilder::init(
    ChoiceEnum::ACKNOWLEDGE_AND_CONTINUE,
    'description_digest0',
    'evaluation_id6'
)->build();
```



