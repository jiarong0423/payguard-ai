# Product Confirm Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVxdWVzdA

ProductConfirmRequest.


# Class Name

`ProductConfirmRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` | getDescription(): string | setDescription(string description): void |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | getEvaluationId(): string | setEvaluationId(string evaluationId): void |
| `productId` | string | Required | This is a container for any-of cases. | getProductId(): string | setProductId(string productId): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ProductConfirmRequestBuilder;

$productConfirmRequest = ProductConfirmRequestBuilder::init(
    'description6',
    'evaluation_id8',
    'String1'
)->build();
```



