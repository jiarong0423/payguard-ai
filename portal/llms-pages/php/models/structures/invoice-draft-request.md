# Invoice Draft Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlcXVlc3Q

InvoiceDraftRequest.


# Class Name

`InvoiceDraftRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `amount` | `string` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` | getAmount(): string | setAmount(string amount): void |
| `currency` | [`string(CurrencyEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/currency.md) | Required | Currency. | getCurrency(): string | setCurrency(string currency): void |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` | getDescription(): string | setDescription(string description): void |
| `payloadDigest` | `string` | Required | Payload digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getPayloadDigest(): string | setPayloadDigest(string payloadDigest): void |
| `reviewToken` | `string` | Required | Review token.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128` | getReviewToken(): string | setReviewToken(string reviewToken): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\InvoiceDraftRequestBuilder;
use TradeGlotLocalConsoleLib\Models\CurrencyEnum;

$invoiceDraftRequest = InvoiceDraftRequestBuilder::init(
    'amount6',
    CurrencyEnum::JPY,
    'description4',
    'payload_digest6',
    'review_token2'
)->build();
```



