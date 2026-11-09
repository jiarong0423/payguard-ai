# Invoice Review Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXF1ZXN0

InvoiceReviewRequest.


# Class Name

`InvoiceReviewRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `acknowledgementToken` | string\|null | Optional | This is a container for any-of cases. | getAcknowledgementToken(): ?string | setAcknowledgementToken(?string acknowledgementToken): void |
| `amount` | `string` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` | getAmount(): string | setAmount(string amount): void |
| `confirmSandboxDraft` | `bool` | Required | Confirm sandbox draft. | getConfirmSandboxDraft(): bool | setConfirmSandboxDraft(bool confirmSandboxDraft): void |
| `currency` | [`string(CurrencyEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/currency.md) | Required | Currency. | getCurrency(): string | setCurrency(string currency): void |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` | getDescription(): string | setDescription(string description): void |
| `descriptionDigest` | string\|null | Optional | This is a container for any-of cases. | getDescriptionDigest(): ?string | setDescriptionDigest(?string descriptionDigest): void |
| `evaluationId` | string\|null | Optional | This is a container for any-of cases. | getEvaluationId(): ?string | setEvaluationId(?string evaluationId): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\InvoiceReviewRequestBuilder;
use TradeGlotLocalConsoleLib\Models\CurrencyEnum;

$invoiceReviewRequest = InvoiceReviewRequestBuilder::init(
    'amount8',
    false,
    CurrencyEnum::USD,
    'description6'
)
    ->acknowledgementToken(
        'String7'
    )
    ->descriptionDigest(
        'String5'
    )
    ->evaluationId(
        'String1'
    )
    ->build();
```



