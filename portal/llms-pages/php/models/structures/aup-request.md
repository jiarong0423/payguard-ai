# Aup Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkF1cFJlcXVlc3Q

AupRequest.


# Class Name

`AupRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` | getDescription(): string | setDescription(string description): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AupRequestBuilder;

$aupRequest = AupRequestBuilder::init(
    'description8'
)->build();
```



