# Invoice Review Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXNwb25zZQ

InvoiceReviewResponse.


# Class Name

`InvoiceReviewResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `action` | `string` | Required, Constant | Action.<br><br>**Value**: `'create_sandbox_invoice_draft'` | getAction(): string | setAction(string action): void |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` | getAdvisoryOnly(): string | setAdvisoryOnly(string advisoryOnly): void |
| `authenticatedActor` | `string` | Required, Constant | Authenticated actor.<br><br>**Value**: `'False'` | getAuthenticatedActor(): string | setAuthenticatedActor(string authenticatedActor): void |
| `expiresAt` | `string` | Required | Expires at. | getExpiresAt(): string | setExpiresAt(string expiresAt): void |
| `limitations` | `string[]` | Required | Limitations. | getLimitations(): array | setLimitations(array limitations): void |
| `payloadDigest` | `string` | Required | Payload digest. | getPayloadDigest(): string | setPayloadDigest(string payloadDigest): void |
| `policyStatus` | `string` | Required, Constant | Policy status.<br><br>**Value**: `'manual_review'` | getPolicyStatus(): string | setPolicyStatus(string policyStatus): void |
| `reviewToken` | `string` | Required | Review token. | getReviewToken(): string | setReviewToken(string reviewToken): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\InvoiceReviewResponseBuilder;

$invoiceReviewResponse = InvoiceReviewResponseBuilder::init(
    'expires_at8',
    [
        'limitations5',
        'limitations6'
    ],
    'payload_digest8',
    'review_token6'
)->build();
```



