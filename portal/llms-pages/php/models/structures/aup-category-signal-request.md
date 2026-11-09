# Aup Category Signal Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVxdWVzdA

AupCategorySignalRequest.


# Class Name

`AupCategorySignalRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` | getDescription(): string | setDescription(string description): void |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | getEvaluationId(): string | setEvaluationId(string evaluationId): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AupCategorySignalRequestBuilder;

$aupCategorySignalRequest = AupCategorySignalRequestBuilder::init(
    'description0',
    'evaluation_id4'
)->build();
```



