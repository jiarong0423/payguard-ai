# Product Reference Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXF1ZXN0

ProductReferenceRequest.


# Class Name

`ProductReferenceRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` | getDescription(): string | setDescription(string description): void |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | getEvaluationId(): string | setEvaluationId(string evaluationId): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ProductReferenceRequestBuilder;

$productReferenceRequest = ProductReferenceRequestBuilder::init(
    'description8',
    'evaluation_id2'
)->build();
```



