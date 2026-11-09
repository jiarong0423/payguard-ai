# Add Tracking Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVxdWVzdA

AddTrackingRequest.


# Class Name

`AddTrackingRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `caseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` | getCaseRef(): string | setCaseRef(string caseRef): void |
| `confirmToken` | string\|null | Optional | This is a container for any-of cases. | getConfirmToken(): ?string | setConfirmToken(?string confirmToken): void |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | getDisputeId(): string | setDisputeId(string disputeId): void |
| `submit` | `?bool` | Optional | Submit.<br><br>**Default**: `false` | getSubmit(): ?bool | setSubmit(?bool submit): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AddTrackingRequestBuilder;

$addTrackingRequest = AddTrackingRequestBuilder::init(
    'case_ref4',
    'dispute_id2'
)
    ->confirmToken(
        'String1'
    )
    ->submit(false)
    ->build();
```



